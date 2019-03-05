const botui = new BotUI('bot');
const client = new ApiAi.ApiAiClient({ accessToken: 'e69258c6563f4f96b370d78591394c80' });

const cache = {
    aol: '',
    description: ''
}

const translation = {
    'greeting': {
        'en.htm': 'Hello there! Looks like you are looking for a lawyer',
        'ch.htm': '你好！看起来你正在寻找律师',
        'my.htm': 'Apa khabar di sana! Sepertinya anda sedang mencari peguam',
        'tm.htm': 'வணக்கம்! நீங்கள் ஒரு வழக்கறிஞரை தேடுகிறீர்களே'
    },
    'area_of_law': {
        'en.htm': 'Which area of law?',
        'ch.htm': '哪个法律领域？',
        'my.htm': 'Kawasan undang-undang yang mana?',
        'tm.htm': 'சட்டத்தின் எந்த பகுதி?'
    },
    'yes': {
        'en.htm': 'Yes',
        'ch.htm': '是',
        'my.htm': 'ya',
        'tm.htm': 'ஆம்'
    },
    'no': {
        'en.htm': 'No',
        'ch.htm': '没必要',
        'my.htm': 'tidak perlu',
        'tm.htm': 'தேவை இல்லை'
    },
    'ask_legal_aid': {
        'en.htm': 'Do you need Legal Aid?',
        'ch.htm': '你需要法律援助吗？',
        'my.htm': 'Adakah anda perlukan Bantuan Perundangan?',
        'tm.htm': 'உங்களுக்கு சட்ட உதவி தேவையா?'
    },
    'tell_me_more': {
        'en.htm': 'Tell us more about your case.',
        'ch.htm': '告诉我们您的案例。',
        'my.htm': 'Beritahu kami lebih lanjut mengenai kes anda.',
        'tm.htm': 'உங்கள் விஷயத்தைப் பற்றி மேலும் சொல்லவும்.'
    },
    'to_better_match': {
        'en.htm': 'So that we can better match the best lawyers to you.',
        'ch.htm': '这样我们就能更好地匹配最优秀的律师。',
        'my.htm': 'Sehingga kita boleh lebih baik memadankan peguam terbaik kepada anda.',
        'tm.htm': 'அதனால் நாங்கள் உங்களுக்கு சிறந்த வழக்கறிஞர்கள் பொருந்தும் முடியும்.'
    },
    'write_here': {
        'en.htm': 'Write here ... ',
        'ch.htm': '写在这里 ...',
        'my.htm': 'Tulis di sini ...',
        'tm.htm': 'இங்கே எழுது ...'
    },
    'tell_again': {
        'en.htm': 'I could not understand. Can we describe your case to me again?',
        'ch.htm': '我无法理解。我们能再次向你描述一下你的情况吗？',
        'my.htm': 'Saya tidak faham. Bolehkah kita menerangkan kes anda kepada saya lagi?',
        'tm.htm': 'எனக்கு புரியவில்லை. உங்கள் வழக்கை மீண்டும் எனக்கு விவரிக்க முடியுமா?'
    },
    'reload_now': {
        'en.htm': 'I still could not get your description. Bye bye.',
        'ch.htm': '我仍然无法得到你的描述。再见。',
        'my.htm': 'Saya masih tidak dapat mendapatkan keterangan anda. Selamat tinggal.',
        'tm.htm': 'நான் இன்னும் உங்கள் விளக்கத்தை பெற முடியவில்லை. பாய் பாய்.'
    }
}

const lang_id = window.location.href.slice(window.location.href.lastIndexOf('/') + 1, -1);

ask_what_type_of_law(
    show_choices_of_lawyers(
        ask_whether_need_legal_aid
    )
);

function ask_whether_need_legal_aid(law_type) {
    botui.message.add({
        delay: 1000,
        content: translation['ask_legal_aid'][lang_id]
    }).then(function () {
        return botui.action.button({
            delay: 1000,
            action: [{
                text: translation['yes'][lang_id],
                value: true
            }, {
                text: translation['no'][lang_id],
                value: false
            }]
        })
    })
        .then(function (needLegalAid) {
            if (needLegalAid.value) {
                botui.message.add({
                    delay: 1000,
                    content: translation['tell_me_more'][lang_id]
                })
                if (cache['aol'] === 'criminal') {
                    window.location.replace('http://probono.lawsociety.org.sg/Pages/Criminal-Legal-Aid-Scheme.aspx');
                } else {
                    window.location.replace('https://www.mlaw.gov.sg/eservices/labesvc/')
                }
            } else {
                botui.message.add({
                    delay: 1000,
                    content: translation['tell_me_more'][lang_id]
                }).then(function () {
                    botui.message.add({
                        delay: 1000,
                        content: translation['to_better_match'][lang_id]
                    });
                }).then(function () {
                    botui.action.text({
                        delay: 2000,
                        action: {
                            size: 50,
                            placeholder: translation['write_here'][lang_id]
                        }
                    })
                        .then(function (result) {
                            if (lang_id !== 'en.htm') {
                                console.log(result.value);
                                axios.post('http://178.128.124.131:8000/translate/', {
                                    text: result.value
                                })
                                    .then(function (response_translate) {

                                        const end = 100;
                                        console.log(response_translate.data.slice(0, end))
                                        
                                        client.textRequest(response_translate.data.slice(0, end))
                                            .then(function (resp) {
                                                console.log(resp.result.metadata.intentName)
                                                if (resp.result.metadata.intentName != 'Default Fallback Intent') {
                                                    cache['description'] = result.value;
                                                    console.log(resp);
                                                    window.localStorage.setItem('lawyers', JSON.stringify(resp.result.fulfillment.messages.slice(0, 6)));
                                                    window.location.replace('/lawyers.html');
                                                }
                                                console.log(cache['description'].length);
                                                if (resp.result.metadata.intentName != 'Default Fallback Intent' && cache['description'].length < 80) {
                                                    cache['description'] += result.value;
                                                    botui.message.add({
                                                        delay: 1000,
                                                        content: 'By writing more we can better match lawyers with similar cases'
                                                    })
                                                        .then(function () {
                                                            botui.action.text({
                                                                delay: 1000,
                                                                action: {
                                                                    size: 50,
                                                                    placeholder: translation['write_here'][lang_id]
                                                                }
                                                            })
                                                                .then(function (result) {
                                                                    if (resp.result.metadata.intentName != 'Default Fallback Intent') {
                                                                        cache['description'] += result.value;
                                                                    }

                                                                    client.textRequest(cache['description'])
                                                                        .then(function (resp) {
                                                                            console.log(resp)
                                                                        })
                                                                })
                                                        })
                                                }

                                                if (resp.result.metadata.intentName == 'Default Fallback Intent') {
                                                    botui.message.add({
                                                        delay: 1000,
                                                        content: translation['tell_again'][lang_id]
                                                    })
                                                        .then(function () {
                                                            botui.action.text({
                                                                delay: 1000,
                                                                action: {
                                                                    size: 50,
                                                                    placeholder: translation['write_here'][lang_id]
                                                                }
                                                            })
                                                                .then(function (result) {
                                                                    client.textRequest(result.value)
                                                                        .then(function (resp) {
                                                                            if (resp.result.metadata.intentName == 'Default Fallback Intent') {
                                                                                botui.message.add({
                                                                                    delay: 1000,
                                                                                    content: translation['reload_now'][lang_id]
                                                                                });
                                                                                setTimeout(function () {
                                                                                    window.location.reload();
                                                                                }, 2000);
                                                                            } else {
                                                                                cache['description'] += result.value;
                                                                                client.textRequest(cache['description'])
                                                                                    .then(function (resp) {
                                                                                        console.log(resp)
                                                                                    })
                                                                            }
                                                                        })
                                                                })
                                                        })
                                                }
                                            })
                                            .catch(function (error) {
                                                console.log(error);
                                            });
                                    })
                                    .catch(function (error) {
                                        console.log(error);
                                    });
                            } else {
                                client.textRequest(result.value)
                                    .then(function (resp) {
                                        console.log(resp.result.metadata.intentName)
                                        if (resp.result.metadata.intentName != 'Default Fallback Intent') {
                                            cache['description'] = result.value;
                                            console.log(resp);
                                            window.localStorage.setItem('lawyers', JSON.stringify(resp.result.fulfillment.messages.slice(0, 6)));
                                            window.location.replace('/lawyers.html');
                                        }
                                        console.log(cache['description'].length);
                                        if (resp.result.metadata.intentName != 'Default Fallback Intent' && cache['description'].length < 80) {
                                            cache['description'] += result.value;
                                            botui.message.add({
                                                delay: 1000,
                                                content: 'By writing more we can better match lawyers with similar cases'
                                            })
                                                .then(function () {
                                                    botui.action.text({
                                                        delay: 1000,
                                                        action: {
                                                            size: 50,
                                                            placeholder: translation['write_here'][lang_id]
                                                        }
                                                    })
                                                        .then(function (result) {
                                                            if (resp.result.metadata.intentName != 'Default Fallback Intent') {
                                                                cache['description'] += result.value;
                                                            }

                                                            client.textRequest(cache['description'])
                                                                .then(function (resp) {
                                                                    console.log(resp)
                                                                })
                                                        })
                                                })
                                        }

                                        if (resp.result.metadata.intentName == 'Default Fallback Intent') {
                                            botui.message.add({
                                                delay: 1000,
                                                content: translation['tell_again'][lang_id]
                                            })
                                                .then(function () {
                                                    botui.action.text({
                                                        delay: 1000,
                                                        action: {
                                                            size: 50,
                                                            placeholder: translation['write_here'][lang_id]
                                                        }
                                                    })
                                                        .then(function (result) {
                                                            client.textRequest(result.value)
                                                                .then(function (resp) {
                                                                    if (resp.result.metadata.intentName == 'Default Fallback Intent') {
                                                                        botui.message.add({
                                                                            delay: 1000,
                                                                            content: translation['reload_now'][lang_id]
                                                                        });
                                                                        setTimeout(function () {
                                                                            window.location.reload();
                                                                        }, 2000);
                                                                    } else {
                                                                        cache['description'] += result.value;
                                                                        client.textRequest(cache['description'])
                                                                            .then(function (resp) {
                                                                                console.log(resp)
                                                                            })
                                                                    }
                                                                })
                                                        })
                                                })
                                        }
                                    })
                                    .catch(function (error) {
                                        console.log(error);
                                    });
                            }


                        });
                })
            }
        });
}

function show_choices_of_lawyers(next_step) {
    botui.action.select({
        delay: 2000,
        action: {
            placeholder: "",
            value: 'family',
            searchselect: true,
            label: 'text',
            options: aol[lang_id],
            button: {
                icon: 'check',
                label: 'OK'
            }
        }
    })
        // botui.action.button({
        //     action: lawyer_types
        // })
        .then(function (result) {
            cache['aol'] = result.value;
            next_step(result);
        });
}

function ask_what_type_of_law(next_step) {
    botui.message.add({
        delay: 1000,
        content: translation['greeting'][lang_id]
    })
        .then(function () {
            botui.message.add({
                delay: 1000,
                content: translation['area_of_law'][lang_id]
            })
                .then(next_step);
        });
}