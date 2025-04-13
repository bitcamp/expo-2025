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

        for (const team of processedData) {
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

            await Promise.all([
                ddb.put(params).promise(),
                sendConfirmationEmail(params.Item),
            ]);
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