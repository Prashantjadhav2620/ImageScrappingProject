
const SLACK_TOKEN = Cypress.env("SLACK_TOKEN");

export function pushToSlack(channelId, arrayOfFailedScenarios) {
    
    const messageBody = {
        text: `Attention <!channel> :rotating_light: :rotating_light: some tests are failed on pj environment. Please check the thread for logs :eyes: `,
    };

    
    cy.request({
        method: 'POST',
        url: 'https://slack.com/api/chat.postMessage',
        headers: {
            // 'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Type': 'application/json; charset=utf-8',
            Authorization: `Bearer ${SLACK_TOKEN}`,
        },
        body: {
            ...messageBody,
            channel: channelId,
        },
    }).then((response) => {
        if (response.body.ok) {
            const threadId = response.body.ts;
            
        arrayOfFailedScenarios.forEach(async (scenario) => {
            const requestBody = {
                text: "failing scenarios",
                blocks: [
                    {
                        type: "section",
                        text: {
                            type: "mrkdwn",
                            text: `Hey :exclamation: :exclamation: :exclamation: ${scenario.scenarioName} is failed`
                        }
                    },
                    {
                        type: "section",
                        text: {
                            type: "mrkdwn",
                            text: `Error ==> \`\`\`${JSON.stringify(scenario.error).substring(0, 2800)}\`\`\``
                        }
                    }
                ],
                channel: channelId,
                thread_ts: threadId,
            };
            
        cy.request({
          method: 'POST',
          url: 'https://slack.com/api/chat.postMessage',
          headers: {
            'Content-Type': 'application/json; charset=utf-8',
            Authorization: `Bearer ${SLACK_TOKEN}`,
          },
          body: requestBody,
        });
      });
    } else {
      console.error('Error posting initial message to Slack:', response.body);
    }
  })
}
