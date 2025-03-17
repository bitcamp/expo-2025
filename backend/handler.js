const withSentry = require('serverless-sentry-lib');
const AWS = require('aws-sdk');
const csv = require('csvtojson');
const UUID = require('uuid');
const fs = require('fs');

AWS.config.update({ region: 'us-east-1' });

const HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Credentials': true,
  'Access-Control-Allow-Headers': '*',
};


module.exports.get_schedule = withSentry(async (event) => {
  const ddb = new AWS.DynamoDB.DocumentClient();
  const params = {
    TableName: process.env.EXPO_TABLE,
  };

  const result = await ddb.scan(params).promise();

  // Returns status code 200 and JSON string of 'result'
  return {
    statusCode: 200,
    body: JSON.stringify(result.Items),
    headers: HEADERS,
  };
});

// Read the JSON data from the file
fs.readFile('./components/alg.json', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading the file:', err);
    return;
  }

  // Parse the JSON data
  const parsedData = JSON.parse(data);

  // Function to format the time to "HH:MM"
  function formatTime(timeString) {
    const date = new Date(timeString);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
  }

  // Process the data into the required format for DynamoDB
  const processedData = parsedData.map(item => {
    const challenges = item.challenges.map(challenge => {
      const formattedStartTime = formatTime(challenge.start_time); // Get the formatted time

      return {
        M: {
          judge: { S: challenge.judge },
          sponsor_name: { S: challenge.company },
          challenge_name: { S: challenge.challenge_name },
          time_slot: { S: formattedStartTime }, // Use the formatted time
        },
      };
    });

    const emails = Array.isArray(item.emails) ? item.emails.filter(email => email !== "").map(email => ({ S: email })) : [];

    return {
      id: item.id.toString(),
      challenges: challenges,
      emails: emails,
      is_in_person: item.in_person,
      project_link: item.link,
      table_assignment: item.table,
      team_name: item.team_name,
    };
  });

  console.log(JSON.stringify(processedData, null, 2));
});

function unmarshallDynamoDB(attribute) {
  if (attribute === null || attribute === undefined) {
    return attribute;
  }
  // 1) Strings
  if (attribute.S !== undefined) {
    return attribute.S;
  }
  // 2) Numbers
  if (attribute.N !== undefined) {
    return Number(attribute.N);
  }
  // 3) Booleans
  if (attribute.BOOL !== undefined) {
    return attribute.BOOL;
  }
  // 4) Null
  if (attribute.NULL !== undefined) {
    return null;
  }
  // 5) Lists
  if (attribute.L !== undefined) {
    return attribute.L.map(unmarshallDynamoDB);
  }
  // 6) Maps
  if (attribute.M !== undefined) {
    const obj = {};
    for (const [key, val] of Object.entries(attribute.M)) {
      obj[key] = unmarshallDynamoDB(val);
    }
    return obj;
  }
  // 7) String sets, number sets, etc. (if needed)
  if (attribute.SS !== undefined) {
    return attribute.SS;
  }
  if (attribute.NS !== undefined) {
    return attribute.NS.map(Number);
  }

  // fallback:
  return attribute;
}

module.exports.post_schedule = withSentry(async (event) => {
  const ddb = new AWS.DynamoDB.DocumentClient();
  try {

    const processedData = JSON.parse(event.body);
    for (const team of processedData) {
      const convertedChallenges = (team.challenges || []).map((challengeObj) =>
        unmarshallDynamoDB(challengeObj) 
      );

      const convertedEmails = (team.emails || []).map((emailObj) =>
        unmarshallDynamoDB(emailObj)
      );

      const params = {
        TableName: process.env.EXPO_TABLE,
        Item: {
          id: team.id, 
          team_name: team.team_name,
          table_assignment: team.table_assignment,
          is_in_person: team.is_in_person, 
          project_link: team.project_link,
          challenges: convertedChallenges,  
          emails: convertedEmails,         
        },
      };

      await ddb.put(params).promise();
    }

    return {
      statusCode: 200,
      headers: HEADERS,
      body: JSON.stringify({
        message: 'All teams inserted successfully using DocumentClient!',
      }),
    };
  } catch (error) {
    console.error('Error inserting teams:', error);
    return {
      statusCode: 500,
      headers: HEADERS,
      body: JSON.stringify({ error: 'Failed to insert teams' }),
    };
  }
});