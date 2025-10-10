from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
import random
import math
import os
import json

app = Flask(__name__)
CORS(app)

print("🚀 راه‌اندازی سیستم با دیتابیس فایل‌محل")

# --- مسیرهای نسبی ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'templates')
IMAGES_FOLDER = os.path.join(STATIC_FOLDER, 'images')

# ایجاد پوشه‌ها اگر وجود ندارند
os.makedirs(IMAGES_FOLDER, exist_ok=True)
os.makedirs(TEMPLATES_FOLDER, exist_ok=True)

# --- دیتابیس فایل‌محل ---
class FileDB:
    def __init__(self, db_file="repair_database.json"):
        self.db_file = db_file
        self.data = self._load_data()
    
    def _load_data(self):
        """بارگذاری داده‌ها از فایل"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ داده‌ها از {self.db_file} بارگذاری شد")
                    return data
            else:
                print("🔶 فایل دیتابیس وجود ندارد، ایجاد داده‌های پیش‌فرض")
                return self._get_default_data()
        except Exception as e:
            print(f"❌ خطا در بارگذاری دیتابیس: {e}")
            return self._get_default_data()
    
    def _get_default_data(self):
        """داده‌های پیش‌فرض"""
        return {
            "repair_jobs": [
                {
                    "id": "A1", 
                    "location": "خیابان ولیعصر، نرسیده به میدان ولیعصر", 
                    "priority": "high", 
                    "specialties": ["روشنایی معابر"], 
                    "crewCapacity": 4, 
                    "status": "scheduled", 
                    "timeLimit": 3,
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "id": "A2", 
                    "location": "میدان انقلاب، خیابان کارگر شمالی", 
                    "priority": "medium", 
                    "specialties": ["شبکه هوایی"], 
                    "crewCapacity": 6, 
                    "status": "scheduled", 
                    "timeLimit": 5,
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "repair_teams": [
                {
                    "teamId": "G1", 
                    "teamName": "روشنایی", 
                    "crewId": "C1", 
                    "crewMembers": 3, 
                    "workStation": "ایستگاه مرکزی منطقه ۶", 
                    "dailyCapacity": 5.5, 
                    "workShift": "daily",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "teamId": "G2", 
                    "teamName": "هوایی", 
                    "crewId": "C1", 
                    "crewMembers": 4, 
                    "workStation": "ایستگاه منطقه ۱۱", 
                    "dailyCapacity": 6, 
                    "workShift": "daily",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "locations": [
                {
                    "name": "ایستگاه مرکزی منطقه ۶", 
                    "lat": 35.7152, 
                    "lng": 51.4050, 
                    "type": "station",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "name": "ایستگاه منطقه ۱۱", 
                    "lat": 35.6892, 
                    "lng": 51.3740, 
                    "type": "station",
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }
    
    def _save_to_file(self):
        """ذخیره داده‌ها در فایل"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print(f"💾 داده‌ها در {self.db_file} ذخیره شد")
            return True
        except Exception as e:
            print(f"❌ خطا در ذخیره دیتابیس: {e}")
            return False
    
    def save(self, collection, data_list):
        """ذخیره داده‌ها در دیتابیس"""
        self.data[collection] = data_list
        print(f"✅ ذخیره {len(data_list)} آیتم در {collection}")
        return self._save_to_file()
    
    def load(self, collection):
        """بارگذاری داده‌ها از دیتابیس"""
        data = self.data.get(collection, [])
        print(f"✅ بارگذاری {len(data)} آیتم از {collection}")
        return data
    
    def get_all_data(self):
        """دریافت تمام داده‌ها"""
        return self.data

# ایجاد نمونه دیتابیس
db = FileDB("repair_database.json")

# --- توابع اصلی برنامه ---
def calculate_real_travel_time(loc1, loc2):
    """تابع واقعی‌تر برای محاسبه زمان سفر"""
    lat1, lon1 = loc1
    lat2, lon2 = loc2
    
    distance_km = math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111
    base_time = distance_km * 3
    traffic_factor = random.uniform(1.2, 2.0)
    travel_time = int(base_time * traffic_factor)
    
    return max(5, min(travel_time, 120))

def format_time(minutes):
    """تبدیل دقیقه به فرمت HH:MM"""
    start_of_day = datetime(1, 1, 1, 0, 0, 0)
    time_delta = timedelta(minutes=minutes)
    return (start_of_day + time_delta).strftime("%H:%M")

def create_output_structure(assignments, assignment_type):
    """تابع کمکی برای ساختاردهی خروجی JSON نهایی"""
    final_output = {"team_assignments": [], "type_applied": assignment_type}
    
    total_travel_all = 0
    total_work_all = 0
    team_counts = []
    
    for team_id, data in assignments.items():
        total_travel = sum(job['travel_time_min'] for job in data['route'])
        total_work = sum(job['job_duration_min'] for job in data['route'])
        total_travel_all += total_travel
        total_work_all += total_work
        team_counts.append(len(data['route']))
        
        final_output['team_assignments'].append({
            "team_id": team_id,
            "route": data['route'],
            "total_travel_time_min": total_travel,
            "total_work_time_min": total_work,
            "total_duration_min": total_travel + total_work,
            "job_count": len(data['route'])
        })
    
    final_output["summary"] = {
        "total_teams": len(assignments),
        "total_travel_time": total_travel_all,
        "total_work_time": total_work_all,
        "average_jobs_per_team": sum(team_counts) / len(team_counts) if team_counts else 0,
        "min_jobs_per_team": min(team_counts) if team_counts else 0,
        "max_jobs_per_team": max(team_counts) if team_counts else 0
    }
    
    return final_output

# --- توابع تخصیص ---
def generate_random_assignment(jobs, teams):
    """۱. تخصیص تصادفی"""
    assignments = {team['teamId']: {"route": [], "current_time": 480, "current_location": (35.7, 51.4)} for team in teams}
    
    for job in jobs:
        qualified_teams = [t for t in teams if any(spec in t.get('teamName', '') for spec in job.get('specialties', []))]
        if not qualified_teams:
            continue
            
        team = random.choice(qualified_teams)
        team_id = team['teamId']
        team_assignment = assignments[team_id]
        
        # موقعیت تصادفی برای شبیه‌سازی
        job_location = (35.69 + random.random() * 0.1, 51.38 + random.random() * 0.1)
        travel_time = calculate_real_travel_time(team_assignment['current_location'], job_location)
        
        job_duration = job.get('crewCapacity', 4) * 60
        start_time_candidate = team_assignment['current_time'] + travel_time
        job_start_time = max(start_time_candidate, 480)
        job_end_time = job_start_time + job_duration
        
        if job_end_time <= 840:
            team_assignment['current_time'] = job_end_time
            team_assignment['current_location'] = job_location
            
            team_assignment['route'].append({
                "job_id": job['id'], 
                "start_time": format_time(job_start_time), 
                "end_time": format_time(job_end_time),
                "travel_time_min": travel_time, 
                "job_duration_min": job_duration,
                "specialty": ', '.join(job.get('specialties', [])),
                "priority": job.get('priority', 'normal')
            })
    
    return create_output_structure(assignments, "random")

def generate_shortest_travel_assignment(jobs, teams):
    """۲. تخصیص بر اساس کمترین زمان سفر"""
    assignments = {team['teamId']: {"route": [], "current_time": 480, "current_location": (35.7, 51.4)} for team in teams}
    
    for job in jobs:
        best_team = None
        best_travel_time = float('inf')
        
        for team in teams:
            if not any(spec in t.get('teamName', '') for spec in job.get('specialties', [])):
                continue
                
            team_id = team['teamId']
            team_assignment = assignments[team_id]
            
            job_location = (35.69 + random.random() * 0.1, 51.38 + random.random() * 0.1)
            travel_time = calculate_real_travel_time(team_assignment['current_location'], job_location)
            
            if travel_time < best_travel_time:
                best_team = team
                best_travel_time = travel_time
        
        if best_team:
            team_id = best_team['teamId']
            team_assignment = assignments[team_id]
            
            job_location = (35.69 + random.random() * 0.1, 51.38 + random.random() * 0.1)
            travel_time = calculate_real_travel_time(team_assignment['current_location'], job_location)
            job_duration = job.get('crewCapacity', 4) * 60
            start_time_candidate = team_assignment['current_time'] + travel_time
            job_start_time = max(start_time_candidate, 480)
            job_end_time = job_start_time + job_duration
            
            if job_end_time <= 840:
                team_assignment['current_time'] = job_end_time
                team_assignment['current_location'] = job_location
                
                team_assignment['route'].append({
                    "job_id": job['id'], 
                    "start_time": format_time(job_start_time), 
                    "end_time": format_time(job_end_time),
                    "travel_time_min": travel_time, 
                    "job_duration_min": job_duration,
                    "specialty": ', '.join(job.get('specialties', [])),
                    "priority": job.get('priority', 'normal')
                })
    
    return create_output_structure(assignments, "shortest_travel")

def generate_balanced_load_assignment(jobs, teams):
    """۳. تخصیص بر اساس توزیع بار متعادل"""
    assignments = {team['teamId']: {"route": [], "current_time": 480, "current_location": (35.7, 51.4)} for team in teams}
    
    for job in jobs:
        best_team = None
        best_score = float('inf')
        
        for team in teams:
            if not any(spec in t.get('teamName', '') for spec in job.get('specialties', [])):
                continue
                
            team_id = team['teamId']
            team_assignment = assignments[team_id]
            
            current_workload = sum(j['job_duration_min'] for j in team_assignment['route'])
            job_location = (35.69 + random.random() * 0.1, 51.38 + random.random() * 0.1)
            travel_time = calculate_real_travel_time(team_assignment['current_location'], job_location)
            
            job_duration = job.get('crewCapacity', 4) * 60
            start_time_candidate = team_assignment['current_time'] + travel_time
            job_start_time = max(start_time_candidate, 480)
            job_end_time = job_start_time + job_duration
            
            if job_end_time <= 840:
                score = current_workload + (travel_time * 0.5)
                
                if score < best_score:
                    best_team = team
                    best_score = score
        
        if best_team:
            team_id = best_team['teamId']
            team_assignment = assignments[team_id]
            
            job_location = (35.69 + random.random() * 0.1, 51.38 + random.random() * 0.1)
            travel_time = calculate_real_travel_time(team_assignment['current_location'], job_location)
            job_duration = job.get('crewCapacity', 4) * 60
            start_time_candidate = team_assignment['current_time'] + travel_time
            job_start_time = max(start_time_candidate, 480)
            job_end_time = job_start_time + job_duration
            
            team_assignment['current_time'] = job_end_time
            team_assignment['current_location'] = job_location
            
            team_assignment['route'].append({
                "job_id": job['id'], 
                "start_time": format_time(job_start_time), 
                "end_time": format_time(job_end_time),
                "travel_time_min": travel_time, 
                "job_duration_min": job_duration,
                "specialty": ', '.join(job.get('specialties', [])),
                "priority": job.get('priority', 'normal')
            })
    
    return create_output_structure(assignments, "balanced_load")

# --- روت‌های Flask ---
@app.route('/')
def index():
    """صفحه اصلی فرانت‌اند"""
    return render_template('index.html')

@app.route('/images/<path:filename>')
def serve_images(filename):
    """سرویس دادن عکس‌ها"""
    return send_from_directory(IMAGES_FOLDER, filename)

@app.route('/api/jobs', methods=['POST', 'GET'])
def manage_jobs():
    """مدیریت کارهای تعمیراتی"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            repair_jobs = data.get('repairJobs', [])
            
            for job in repair_jobs:
                if 'timestamp' not in job:
                    job['timestamp'] = datetime.now().isoformat()
            
            db.save("repair_jobs", repair_jobs)
            
            return jsonify({
                "status": "success",
                "message": f"{len(repair_jobs)} کار با موفقیت ذخیره شد",
                "count": len(repair_jobs)
            })
        
        elif request.method == 'GET':
            repair_jobs = db.load("repair_jobs")
            return jsonify({
                "status": "success",
                "jobs": repair_jobs,
                "count": len(repair_jobs)
            })
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"خطا در مدیریت کارها: {str(e)}"}), 500

@app.route('/api/teams', methods=['POST', 'GET'])
def manage_teams():
    """مدیریت تیم‌های تعمیراتی"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            repair_teams = data.get('repairTeams', [])
            
            for team in repair_teams:
                if 'timestamp' not in team:
                    team['timestamp'] = datetime.now().isoformat()
            
            db.save("repair_teams", repair_teams)
            
            return jsonify({
                "status": "success",
                "message": f"{len(repair_teams)} تیم با موفقیت ذخیره شد",
                "count": len(repair_teams)
            })
        
        elif request.method == 'GET':
            repair_teams = db.load("repair_teams")
            return jsonify({
                "status": "success",
                "teams": repair_teams,
                "count": len(repair_teams)
            })
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"خطا در مدیریت تیم‌ها: {str(e)}"}), 500

@app.route('/api/locations', methods=['POST', 'GET'])
def manage_locations():
    """مدیریت موقعیت‌های جغرافیایی"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            locations = data.get('locations', [])
            
            for location in locations:
                if 'timestamp' not in location:
                    location['timestamp'] = datetime.now().isoformat()
            
            db.save("locations", locations)
            
            return jsonify({
                "status": "success",
                "message": f"{len(locations)} موقعیت با موفقیت ذخیره شد",
                "count": len(locations)
            })
        
        elif request.method == 'GET':
            locations = db.load("locations")
            return jsonify({
                "status": "success",
                "locations": locations,
                "count": len(locations)
            })
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"خطا در مدیریت موقعیت‌ها: {str(e)}"}), 500

@app.route('/api/all-data', methods=['POST', 'GET'])
def manage_all_data():
    """مدیریت تمام داده‌ها"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            
            repair_jobs = data.get('repairJobs', [])
            repair_teams = data.get('repairTeams', [])
            locations = data.get('locations', [])
            
            for item in repair_jobs + repair_teams + locations:
                if 'timestamp' not in item:
                    item['timestamp'] = datetime.now().isoformat()
            
            db.save("repair_jobs", repair_jobs)
            db.save("repair_teams", repair_teams)
            db.save("locations", locations)
            
            return jsonify({
                "status": "success",
                "message": "تمام داده‌ها با موفقیت ذخیره شدند",
                "jobs_count": len(repair_jobs),
                "teams_count": len(repair_teams),
                "locations_count": len(locations)
            })
        
        elif request.method == 'GET':
            all_data = db.get_all_data()
            return jsonify({
                "status": "success",
                "repairJobs": all_data["repair_jobs"],
                "repairTeams": all_data["repair_teams"],
                "locations": all_data["locations"],
                "total_count": len(all_data["repair_jobs"]) + len(all_data["repair_teams"]) + len(all_data["locations"])
            })
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"خطا در مدیریت داده‌ها: {str(e)}"}), 500

@app.route('/optimize', methods=['POST'])
def optimize():
    """بهینه‌سازی و تخصیص کارها"""
    try:
        request_data = request.get_json()
        allocation_type = request_data.get('allocation_type', 'random')
        
        repair_jobs = request_data.get('repair_jobs', [])
        repair_teams = request_data.get('repair_teams', [])
        
        if not repair_jobs:
            repair_jobs = db.load("repair_jobs")
        if not repair_teams:
            repair_teams = db.load("repair_teams")
        
        if allocation_type == 'shortest_travel':
            results = generate_shortest_travel_assignment(repair_jobs, repair_teams)
        elif allocation_type == 'balanced_load':
            results = generate_balanced_load_assignment(repair_jobs, repair_teams)
        else:
            results = generate_random_assignment(repair_jobs, repair_teams)
        
        results['planning_info'] = {
            'total_jobs': len(repair_jobs),
            'total_teams': len(repair_teams),
            'algorithm_used': allocation_type,
            'timestamp': datetime.now().isoformat(),
            'deployment_info': 'سیستم یکپارچه با دیتابیس فایل‌محل - توسعه توسط هادی صدوقی یزدی'
        }
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({
            "error": "خطا در پردازش درخواست",
            "message": str(e),
            "deployment_info": "سیستم یکپارچه با دیتابیس فایل‌محل - توسعه توسط هادی صدوقی یزدی"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """بررسی سلامت سیستم"""
    data_counts = {
        "jobs": len(db.load("repair_jobs")),
        "teams": len(db.load("repair_teams")),
        "locations": len(db.load("locations"))
    }
    
    return jsonify({
        "status": "healthy", 
        "message": "سرویس فعال است",
        "database": "دیتابیس فایل‌محل (repair_database.json)",
        "developer": "هادی صدوقی یزدی",
        "timestamp": datetime.now().isoformat(),
        "data_counts": data_counts
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 راه‌اندازی سیستم با دیتابیس فایل‌محل")
    print("=" * 60)
    print("💾 فایل دیتابیس: repair_database.json")
    print("📁 پوشه عکس‌ها: static/images/")
    print("📄 پوشه قالب‌ها: templates/")
    print("🌐 دسترسی داخلی: http://localhost:5000/")
    print("🔗 دسترسی از اینترنت: از طریق Ngrok/LocalTunnel")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)