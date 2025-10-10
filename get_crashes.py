import psycopg2
import math
import utils

def get_crashes_near_me(
    lat: float, lng: float, radius_km: float = 0.5, days_back: int = 60
):
    try:
        # WIP - move this out
        conn = psycopg2.connect(
            host="localhost", database="runsafe_db", user="lpietrewicz", password=""
        )
        cursor = conn.cursor()

        # bounding box for query
        lat_buffer = radius_km / 111.0
        lng_buffer = radius_km / (111.0 * math.cos(math.radians(lat)))

        cursor.execute(
            """
            SELECT collision_id, crash_date, latitude, longitude, injuries, fatalities
            FROM crashes
            WHERE latitude BETWEEN %s AND %s
            AND longitude BETWEEN %s AND %s
        """,
            (lat - lat_buffer, lat + lat_buffer, lng - lng_buffer, lng + lng_buffer),
        )

        rough_crashes = cursor.fetchall()
        conn.close()

        # filter by exact distance
        nearby_crashes = []
        for crash in rough_crashes:
            collision_id, crash_date, crash_lat, crash_lng, injuries, fatalities = crash
            distance = utils.euc_distance(lat, lng, float(crash_lat), float(crash_lng))

            if distance <= radius_km:
                clean_crash = {
                    "crash_id": collision_id,
                    "date": str(crash_date),
                    "distance_km": round(distance, 2),
                    "location": {"lat": float(crash_lat), "lng": float(crash_lng)},
                    "injuries": injuries or 0,
                    "fatalities": fatalities or 0,
                }
                nearby_crashes.append(clean_crash)

        # summary
        safety_score, total_crashes, total_injuries, total_fatalities = safety_wrapper(lat, lng, radius_km, nearby_crashes)

        return {
            "search_location": {"lat": lat, "lng": lng},
            "search_radius_km": radius_km,
            "days_searched": days_back,
            "summary": {
                "total_crashes": total_crashes,
                "total_injuries": total_injuries,
                "total_fatalities": total_fatalities,
            },
            "safety": safety_score
        }

    except Exception as e:
        return {"error": f"Database query failed: {str(e)}"}
