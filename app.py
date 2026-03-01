from flask import Flask, render_template, request, redirect, url_for, flash, Response
import sqlite3
import csv
import io
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'aquanet_survey_secret_2026'

DB_PATH = 'survey.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submitted_at TEXT,
            name TEXT,
            age TEXT,
            role TEXT,
            specialization TEXT,
            experience TEXT,
            region TEXT,
            challenges TEXT,
            data_difficulty TEXT,
            datasets_scattered TEXT,
            tools_used TEXT,
            platform_satisfaction TEXT,
            missing_feature TEXT,
            historical_data_access TEXT,
            map_viz_importance TEXT,
            fisheries_integration TEXT,
            species_data_frequency TEXT,
            aware_integrated_platform TEXT,
            platform_meets_needs TEXT,
            aquanet_usefulness TEXT,
            valuable_features TEXT,
            reduce_search_time TEXT,
            genomics_helpfulness TEXT,
            collab_importance TEXT,
            join_community TEXT,
            share_findings TEXT,
            upload_datasets TEXT,
            data_concerns TEXT,
            doi_importance TEXT,
            citizen_science TEXT,
            conservation_impact TEXT,
            likely_to_use TEXT,
            recommend TEXT,
            unique_feature TEXT,
            improvements TEXT,
            comments TEXT,
            future_testing TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def index():
    return render_template('survey.html')

@app.route('/submit', methods=['POST'])
def submit():
    f = request.form

    data = {
        'submitted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'name': f.get('name', '').strip(),
        'age': f.get('age', '').strip(),
        'role': f.get('role', ''),
        'specialization': f.get('specialization', ''),
        'experience': f.get('experience', ''),
        'region': f.get('region', ''),
        'challenges': ', '.join(f.getlist('challenges')),
        'data_difficulty': f.get('data_difficulty', ''),
        'datasets_scattered': f.get('datasets_scattered', ''),
        'tools_used': ', '.join(f.getlist('tools_used')),
        'platform_satisfaction': f.get('platform_satisfaction', ''),
        'missing_feature': f.get('missing_feature', '').strip(),
        'historical_data_access': f.get('historical_data_access', ''),
        'map_viz_importance': f.get('map_viz_importance', ''),
        'fisheries_integration': f.get('fisheries_integration', ''),
        'species_data_frequency': f.get('species_data_frequency', ''),
        'aware_integrated_platform': f.get('aware_integrated_platform', ''),
        'platform_meets_needs': f.get('platform_meets_needs', ''),
        'aquanet_usefulness': f.get('aquanet_usefulness', ''),
        'valuable_features': ', '.join(f.getlist('valuable_features')),
        'reduce_search_time': f.get('reduce_search_time', ''),
        'genomics_helpfulness': f.get('genomics_helpfulness', ''),
        'collab_importance': f.get('collab_importance', ''),
        'join_community': f.get('join_community', ''),
        'share_findings': f.get('share_findings', ''),
        'upload_datasets': f.get('upload_datasets', ''),
        'data_concerns': ', '.join(f.getlist('data_concerns')),
        'doi_importance': f.get('doi_importance', ''),
        'citizen_science': f.get('citizen_science', ''),
        'conservation_impact': f.get('conservation_impact', ''),
        'likely_to_use': f.get('likely_to_use', ''),
        'recommend': f.get('recommend', ''),
        'unique_feature': f.get('unique_feature', '').strip(),
        'improvements': f.get('improvements', '').strip(),
        'comments': f.get('comments', '').strip(),
        'future_testing': f.get('future_testing', ''),
        'email': f.get('email', '').strip(),
    }

    conn = get_db()
    conn.execute('''
        INSERT INTO responses (
            submitted_at, name, age, role, specialization, experience, region,
            challenges, data_difficulty, datasets_scattered, tools_used,
            platform_satisfaction, missing_feature, historical_data_access,
            map_viz_importance, fisheries_integration, species_data_frequency,
            aware_integrated_platform, platform_meets_needs,
            aquanet_usefulness, valuable_features, reduce_search_time,
            genomics_helpfulness, collab_importance, join_community,
            share_findings, upload_datasets, data_concerns, doi_importance,
            citizen_science, conservation_impact, likely_to_use, recommend,
            unique_feature, improvements, comments, future_testing, email
        ) VALUES (
            :submitted_at, :name, :age, :role, :specialization, :experience, :region,
            :challenges, :data_difficulty, :datasets_scattered, :tools_used,
            :platform_satisfaction, :missing_feature, :historical_data_access,
            :map_viz_importance, :fisheries_integration, :species_data_frequency,
            :aware_integrated_platform, :platform_meets_needs,
            :aquanet_usefulness, :valuable_features, :reduce_search_time,
            :genomics_helpfulness, :collab_importance, :join_community,
            :share_findings, :upload_datasets, :data_concerns, :doi_importance,
            :citizen_science, :conservation_impact, :likely_to_use, :recommend,
            :unique_feature, :improvements, :comments, :future_testing, :email
        )
    ''', data)
    conn.commit()
    conn.close()

    return redirect(url_for('thankyou'))

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/admin')
def admin():
    conn = get_db()
    rows = conn.execute('SELECT * FROM responses ORDER BY submitted_at DESC').fetchall()
    count = conn.execute('SELECT COUNT(*) FROM responses').fetchone()[0]
    conn.close()
    return render_template('admin.html', rows=rows, count=count)

@app.route('/admin/export')
def export_csv():
    conn = get_db()
    rows = conn.execute('SELECT * FROM responses ORDER BY submitted_at DESC').fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)

    if rows:
        writer.writerow(rows[0].keys())
        for row in rows:
            writer.writerow(list(row))

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=aquanet_survey_responses.csv'}
    )

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
