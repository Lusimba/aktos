load_test_data = [
    {
        "id": 10001,
        "street": "578 Blake Street",
        "status": "in_progress",
        "previous_jobs_count": 2,
        "amount_due": 1000,
        "location": (33.41247397, -112.2808169),
    },
    {
        "id": 10002,
        "street": "177 Blake Street",
        "status": "collected",
        "previous_jobs_count": 1,
        "amount_due": 1001,
        "location": (33.45330369, -112.2324871),
    }
]

def get_data():
    return load_test_data
