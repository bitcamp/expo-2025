// Curl command to push to aws table:
// curl --ssl-no-revoke -X POST "https://tnmksukfo2.execute-api.us-east-1.amazonaws.com/dev/expo-2025/schedule" -H "Content-Type: application/json" -d "[]"

const AWS = require('aws-sdk');
const fs = require('fs');
// const bcrypt = require('bcryptjs');
// const crypto = require('crypto');

AWS.config.update({ region: 'us-east-1' });

const HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Credentials': true,
  'Access-Control-Allow-Headers': '*',
};

async function sendConfirmationEmail(team) {
  console.log('Starting to send email for team:', team.team_name);
  const ses = new AWS.SES();


  // For testing, override with  your test emails:
  // const validEmails = [
  //   "test@bitcamp.org",
  // ];

  const validEmails = (team.emails || []).filter(email => email && email.trim() !== "");
  if (validEmails.length === 0) {
    console.log('No valid emails for team:', team.team_name);
    return;
  }



  const params = {
    Destination: { ToAddresses: validEmails },
    Source: "Bitcamp <hello@bit.camp>",
    ConfigurationSetName: "expo-2025",
    Template: "provideId",
    TemplateData: JSON.stringify({
      teamName: team.team_name,
      username: team.id
    })
  };

  console.log('SES params:', params);

  try {
    const result = await ses.sendTemplatedEmail(params).promise();
    console.log('Email sent successfully for team:', team.team_name, result);
    return result;
  } catch (error) {
    console.error(`Error sending email for team ${team.team_name}:`, error);
  }
}

function formatTime(timeString) {
  const date = new Date(timeString);
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  return `${hours}:${minutes}`;
}

// function generateSecureRandomPassword(length = 5) {
//   const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
//   const randomBytes = crypto.randomBytes(length);
//   let password = "";
//   for (let i = 0; i < length; i++) {
//     password += charset.charAt(randomBytes[i] % charset.length);
//   }
//   return password;
// }

// async function generateHashedPassword() {
//   const saltRounds = 3;
//   const plain = generateSecureRandomPassword();
//   const salt = await bcrypt.genSalt(saltRounds);
//   return bcrypt.hash(plain, salt);
// }


module.exports.get_schedule = async (event) => {
  const ddb = new AWS.DynamoDB.DocumentClient();
  const params = {
    TableName: process.env.EXPO_TABLE,
  };

  const result = await ddb.scan(params).promise();

  return {
    statusCode: 200,
    body: JSON.stringify(result.Items),
    headers: HEADERS,
  };
};

// fs.readFile('expo_algorithm_results.json', 'utf8', (err, data) => {
//   if (err) {
//     console.error('Error reading the file:', err);
//     return;
//   }

//   const parsedData = JSON.parse(data);

//   const processedData = await Promise.all(rawData.map(async item => {
//     const challenges = item.challenges.map(challenge => {
//       const formattedStartTime = formatTime(challenge.start_time);
//       return {
//         M: {
//           judge: { S: challenge.judge },
//           sponsor_name: { S: challenge.company },
//           challenge_name: { S: challenge.challenge_name },
//           time_slot: { S: formattedStartTime },
//         },
//       };
//     });

//     const emails = Array.isArray(item.emails)      ? item.emails.filter(email => email !== "").map(email => ({ S: email }))
//       : [];

//     const password = await generateHashedPassword();

//     return {
//       id: item.id.toString(),
//       team_name: item.team_name,
//       table_assignment: item.table,
//       is_in_person: item.in_person,
//       project_link: item.link,
//       challenges: challenges,
//       emails: emails,
//       password: password,
//     };
//   }));

// });

function unmarshallDynamoDB(attribute) {
  if (attribute === null || attribute === undefined) return attribute;
  if (attribute.S !== undefined) return attribute.S;
  if (attribute.N !== undefined) return Number(attribute.N);
  if (attribute.BOOL !== undefined) return attribute.BOOL;
  if (attribute.NULL !== undefined) return null;
  if (attribute.L !== undefined) return attribute.L.map(unmarshallDynamoDB);
  if (attribute.M !== undefined) {
    const obj = {};
    for (const [key, val] of Object.entries(attribute.M)) {
      obj[key] = unmarshallDynamoDB(val);
    }
    return obj;
  }
  if (attribute.SS !== undefined) return attribute.SS;
  if (attribute.NS !== undefined) return attribute.NS.map(Number);
  return attribute;
}

module.exports.post_schedule = async (event) => {
  const ddb = new AWS.DynamoDB.DocumentClient();
  try {
    const fileContents = fs.readFileSync('expo_algorithm_results.json', 'utf8');
    const rawData = JSON.parse(fileContents);

    const processedData = await Promise.all(rawData.map(async item => {
      const challenges = item.challenges.map(challenge => {
        const formattedStartTime = formatTime(challenge.start_time);
        return {
          M: {
            judge: { S: challenge.judge },
            sponsor_name: { S: challenge.company },
            challenge_name: { S: challenge.challenge_name },
            time_slot: { S: formattedStartTime },
          },
        };
      });
      const emails = Array.isArray(item.emails)
        ? item.emails.filter(email => email !== "").map(email => ({ S: email }))
        : [];

      // const hashed = await generateHashedPassword();

      return {
        id: item.id.toString(),
        team_name: item.team_name,
        table_assignment: item.table,
        is_in_person: item.in_person,
        project_link: item.link,
        challenges: challenges,
        emails: emails,
        // password: hashed,
      };
    }));

    const chunkSize = 10;

    for (let i = 0; i < processedData.length; i += chunkSize) {
      const chunk = processedData.slice(i, i + chunkSize);
      await Promise.all(
        chunk.map(async (team) => {
          const convertedChallenges = (team.challenges || []).map(challengeObj =>
            unmarshallDynamoDB(challengeObj)
          );
          const convertedEmails = (team.emails || []).map(emailObj =>
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
              emails: convertedEmails
            },
          };

          await ddb.put(params).promise();
          // await sendConfirmationEmail(params.Item);
        })
      );

      console.log(`Processed chunk from index ${i} to ${i + chunkSize - 1}`);
    }

    return {
      statusCode: 200,
      headers: HEADERS,
      body: JSON.stringify({
        message: 'All teams inserted successfully using DocumentClient!',
        count: processedData.length,
        data: processedData
      }),
    };
  } catch (error) {
    console.error('Error inserting teams:', error);
    return {
      statusCode: 500,
      headers: HEADERS,
      body: JSON.stringify({
        error: 'Failed to insert teams',
        message: error.message,
        stack: error.stack
      }),
    };
  }
};

