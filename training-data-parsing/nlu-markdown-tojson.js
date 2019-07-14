// This converts rasa training markdown to just json with the intent
// classes as intentName and the text body as text.

// NOTE: You must remove any comments from the mardown file for parser to work

const jsonmark = require('jsonmark');
const fs = require('fs');
const markdown = fs.readFileSync('../data/nlu.md', 'utf8');

const parsedMarkdown = jsonmark.parse(markdown);

const items = [];
Object.keys(parsedMarkdown.content).forEach(item => {
    if (item.startsWith('intent:')) {
        const intentName = item.slice(7);
        const bodyItems = parsedMarkdown.content[item].body.split("\n-");
        bodyItems.forEach(body => {
            if (body.startsWith('- ')) {
                body = body.slice(2);
            }
            // for now, let's skip the NER stuff
            if (body.includes('[')) {
                return;
            }
            items.push(
                {
                    intentName,
                    text: body.trim(),
                }
            )
        })
    }
})

console.log(items.length)
const stringed = JSON.stringify(items)
fs.writeFileSync('rasa-intents.json', stringed)