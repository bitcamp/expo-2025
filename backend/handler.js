const withSentry = require('serverless-sentry-lib');
const AWS = require('aws-sdk');
const csv = require('csvtojson');
const UUID = require('uuid');
const fs = require('fs');

AWS.config.update({region: 'us-east-1'});

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
      id: item.id.toString() , 
      challenges: challenges , 
      emails: emails, 
      is_in_person: item.in_person ,
      project_link: item.link ,
      table_assignment: item.table ,
      team_name: item.team_name ,
    };
  });

  console.log(JSON.stringify(processedData, null, 2));
});


module.exports.post_schedule = withSentry(async (event) => {
  const ddb = new AWS.DynamoDB.DocumentClient();
  const body = JSON.parse(event.body);

    // checks if any field is missing to create a  user
  if (!body.email
    || !body.full_name
    || !body.access_level // TODO refactor to `role` instead of `access_level`?
    || !body.group
    || !body.campfire_team) { // Campfire team is a Bitcamp-specific field ('red' | 'green' | 'blue')
    return {
      statusCode: 400,
      body: ' is missing a field',
    };
  }

  // body.combined_values.forEach(entry => {
  //   const is_in_person = entry[0][0]; 
  //   const table_assignment = "";
  //   if (is_in_person === "Yes"){
  //     table = entry[0][1];
  //   }
  //   const team_name = entry[1];


  // });

  const params = {
    TableName: process.env.EXPO_TABLE,
    // Item: {
    //   id: ,
    //   challenge_name: ,
    //   Emails: ,
    //   is_in_person: ,
    //   judge: ,
    //   project_link: ,
    //   sponsor_name: ,
    //   table_assignment: ,
    //   team_name: ,
    //   time_slot: 
    // },
    Item: {},
  };

  // dynamically add post request body params to document
  Object.keys(body).forEach((k) => {
    params.Item[k] = body[k];
  });
  

  body.setRegistrationStatus = true;

  // Send the user an invite email (for Bitcamp, we send the invite emails separately from adding users)
  // await sendLoginLinkEmail(body.id, true, false);

  // Returns status code 200 and JSON string of 'result'
  return {
    statusCode: 200,
    body: JSON.stringify(params.Item),
    headers: HEADERS,
  };
});