from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

WEBHOOK_URL = 'https://hooks.zapier.com/hooks/catch/17552845/3wfk1or/'

@app.route('/', methods=['GET', 'POST'])
def index():
    no_data_found = False

    if request.method == 'POST':
        email = request.form.get('email')
        epoch_id = request.form.get('epoch_id')
        project_id = request.form.get('project_id')

        if email and epoch_id and project_id:
            # Construct the API URL with epoch_id and project_id
            api_url = f'http://localhost:8002/data/{epoch_id}/{project_id}'
            
            # Hit the API
            api_response = requests.get(api_url)
            if api_response.status_code == 200:
                api_data = api_response.json()
                if api_data == "no data found":
                    no_data_found = True
                else:
                    # Include the email with the API data for the webhook
                    webhook_data = {'email': email, 'api_data': api_data}
                    response = requests.post(WEBHOOK_URL, json=webhook_data)
                    return f'API data and email sent to webhook. Status Code: {response.status_code}'
            else:
                return f'Failed to get data from API. Status Code: {api_response.status_code}'
        else:
            return 'Please enter all fields.'

    return render_template_string('''
    <form method="POST">
        Email: <input type="email" name="email" required><br>
        Epoch ID: <input type="text" name="epoch_id" required><br>
        Project ID: <input type="text" name="project_id" required><br>
        <input type="submit" value="Submit">
    </form>
    <script>
        window.onload = function() {
            var noDataFound = "{{ no_data_found }}";
            if (noDataFound == "True") {
                alert("No data found");
            }
        }
    </script>
    ''', no_data_found=no_data_found)

if __name__ == '__main__':
    app.run(debug=True)
