const chat = require('/Users/LHS/Downloads/data_tolokers.json');
const fs = require('fs');
const dialogues = chat.map(item => { return item.dialog })
const flattened = dialogues.reduce(
    ( accumulator, currentValue ) => accumulator.concat(currentValue),
    []
);
const just_human = flattened.filter(item => { return item.sender_class === 'Human'})

console.log(just_human.length)
const stringed = JSON.stringify(just_human)
fs.writeFileSync('human-chat.json', stringed)