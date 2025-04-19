from config import monster_client as client

def generate_image(prompt):
    try:
        model = 'txt2img'  # Replace with the desired model name
        input_data = {
        'prompt': prompt,
        'negprompt': '',
        'samples': 1,
        'steps': 50,
        'aspect_ratio': 'square',
        'guidance_scale': 7.5,
        'seed': 2414,
                    }
        result = client.generate(model, input_data)
    except:
        return None
    else:
        return result['output']

