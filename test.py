import chatgpt


def test_conditional_context():
    rst = chatgpt.conditional_context('./data/fine_tuning_sample_data.json')
    print(rst)


def test_concat_text():
    st_past = [
        "How are you?",
        "Hello world."
    ]
    st_generated = [
        "I am fine.",
        "Why not"
    ]
    upper_bound=5
    rst = chatgpt.concat_text(st_past, st_generated, upper_bound)
    return print(rst)



def test_generate_response():
    prompt = "Do you know other beer beyond ABInbev"
    model = 'gpt-3.5-turbo'
    rst = chatgpt.generate_response(prompt, model)
    print(rst)


if __name__ == "__main__":
    #test_concat_text()
    test_generate_response()
    #test_conditional_context()
