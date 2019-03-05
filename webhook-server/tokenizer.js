const keyword_extractor = require("keyword-extractor");

module.exports = {
    tokenize: function (sentence) {
        const result = keyword_extractor.extract(sentence, {
            language: "english",
            remove_digits: true,
            return_changed_case: true,
            remove_duplicates: false
        });
        return result.slice(0,4).join(' ');
    }
}