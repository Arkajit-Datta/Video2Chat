def html(recipe_json, image_urls, output_file_path):


    html_template = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; background-color: #f4f4f4; color: #333; }}
        .container {{ max-width: 800px; margin: auto; overflow: hidden; padding: 20px; }}
        .header {{ background: #333; color: #fff; text-align: center; padding: 20px 0; }}
        .content {{ padding: 20px; background: #fff; }}
        .step {{ margin-bottom: 20px; }}
        .step-header {{ font-weight: bold; margin-bottom: 10px; font-size: 1.75em; }}
        .step img {{ max-width: 100%; height: auto; width: 60%; margin-top: 10px; font-size: 1em; margin: auto; display: block; }}
        .thoughts {{ background: #f9f9f9; padding: 15px; margin-top: 20px; border-left: 6px solid #333; }}
    </style>
    </head>
    <body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
        </div>
        <div class="content">
            <div class="thoughts">
                <p>{description}</p>
            </div>
            {steps_html}
        </div>
    </div>
    </body>
    </html>"""

    step_template = """
            <div class="step">
                <div class="step-header">Step {step_number}</div>
                <p>{step_description}</p>
                <img src="{image_url}" alt="Step {step_number}">
            </div>
    """

    # Generate HTML for each step including the corresponding image URL
    steps_html = ""
    for i, step in enumerate(recipe_json['recipe']['list_of_steps'], start=1):
        steps_html += step_template.format(
            step_number=i,
            step_description=step['step'],
            image_url=image_urls[i-1]  # assuming the list of URLs matches steps
        )

    html_content = html_template.format(
        title=recipe_json['recipe']['title'],
        description=recipe_json['recipe']['description'],
        thought_on_cooking_style=recipe_json['thought_on_cooking_style'],
        thought_on_recipe=recipe_json['thought_on_recipe'],
        steps_html=steps_html
    )

    # Print or save the HTML content as needed
    with open(output_file_path, 'w') as f:
        f.write(html_content)