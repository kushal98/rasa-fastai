const data = require('./AskUbuntuCorpus.json');
const fs = require('fs');

rasa_json = {
    rasa_nlu_data: {
        common_examples: [],
        regex_features : [],
        lookup_tables  : [],
        entity_synonyms: []
    }
};

const examples = data.sentences;
let errorCount = 0

examples.forEach(example => {
    const rasafied = {
        text: example.text,
        intent: example.intent,
        entities: example.entities.map(item => {
            try {
                // ubuntu seems to be splitting on words and then on each digit
                // in a decimal
                const split_text_on_digit = example.text.split(/(\.\d)/)
                const final_split = split_text_on_digit.reduce((acc, curr) => {
                    const addition = curr.split(' ');
                    return acc.concat(addition)
                }, [])
                // askubuntu data has start and stop based on word
                // whereas rasa is based on char so have to convert
                const { start, stop, text, entity } = item;
        
                const start_word = final_split[start];
                const end_word = final_split[stop];
                const start_char = example.text.indexOf(start_word);
                const end_char = example.text.indexOf(end_word) + end_word.length;
                console.log("text!!", example.text)
                console.log("start!!", start)
                console.log("stop!!", stop)
                console.log("start_word", start_word)
                console.log("end_word", end_word)
                console.log("start_char!!", start_char)
                console.log("end_char!!: ", end_char)
                return {
                    // rasa indexes at letter index of start and then last index + 1
                    start: start_char,
                    end: end_char,
                    value: text,
                    entity: entity,
                }
            } catch(err) {
                // the ubuntu start and stop counting is odd. not clear what
                // the pattern is with 3 examples (so lose 3 entities)
                console.log("err!!", err)
                errorCount++
                return {}
            }
        })
      }
    rasa_json.rasa_nlu_data.common_examples.push(rasafied);
})

// should be 162 examples
console.log(rasa_json.rasa_nlu_data.common_examples.length)
console.log("error count!!", errorCount)
const stringed = JSON.stringify(rasa_json)
fs.writeFileSync('askubuntu_in_rasa_format.json', stringed)