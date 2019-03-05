const express = require('express');
const bodyParser = require('body-parser');
const tokenizer = require('./tokenizer');
const superagent = require('superagent');

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));

app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "*");
    next();
});

app.post('/wb', (req, response) => {
    const q = req.body;
    console.log(q);
    let aol_keywords = q.result.metadata.intentName;
    // if(aol_keywords === 'Default Fallback Intent'){
    //     response.send({
    //         messages: [],
    //         source: "ttt"
    //     })
    //     return;
    // }

    let description = q.result.resolvedQuery
    let kw = tokenizer.tokenize(description);

    console.log(kw)
    
    let load = {
        aol_keywords: aol_keywords,
        intent_keywords: kw
    };

    superagent.post('http://178.128.124.131:8000/aol/')
        .send(load)
        .then(res => {
            console.log(res.body.length);
            response.send({
                messages: res.body,
                source: "ttt"
            });
        });
    
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`))   