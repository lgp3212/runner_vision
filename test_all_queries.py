import get_routes
import get_crashes
import get_weather
import get_closures
import polyline_safety_analysis as psa

def test_all_queries(start_lat, start_lng, target_distance_km):
    """
    Test all data queries together
    """
    print("="*60)
    print("TESTING ALL QUERIES (Worst Case Scenario)")
    print("="*60)
    print(f"Location: ({start_lat}, {start_lng})")
    print(f"Distance: {target_distance_km}km")
    print()
    
    # 1. ROUTE GENERATION
    print("1️⃣  ROUTE GENERATION")
    print("-"*60)
    routes = get_routes.optimized_route_finder(start_lat, start_lng, target_distance_km)
    print(f"✓ Generated {len(routes)} routes")
    for i, route in enumerate(routes, 1):
        print(f"   Route {i}: {route['direction']} - {route['accuracy']:.1f}% accuracy")
    print()
    
    # 2. SAFETY ANALYSIS (for each route)
    print("2️⃣  SAFETY ANALYSIS (Crash Data)")
    print("-"*60)
    enhanced_routes = []
    for i, route in enumerate(routes, 1):
        print(f"   Analyzing route {i}/{len(routes)}...")
        enhanced_route = psa.analyze_route_safety_detailed(route)
        enhanced_routes.append(enhanced_route)
        
        safety_score = enhanced_route["safety_analysis"]["overall_safety_score"]
        dangerous_count = len(enhanced_route["safety_analysis"]["dangerous_segments"])
        print(f"   ✓ Safety score: {safety_score:.1f}/100, Dangerous segments: {dangerous_count}")
    print()
    
    # 3. WEATHER DATA
    print("3️⃣  WEATHER DATA")
    print("-"*60)
    weather = get_weather.get_weather_conditions(start_lat, start_lng)
    weather_risk = get_weather.assess_weather_risk(weather)
    print(f"✓ Weather: {weather.get('description', 'unknown')}, {weather.get('temperature_f', 0):.0f}°F")
    print(f"✓ Visibility: {weather.get('visibility_meters', 0)}m")
    print(f"✓ Risk level: {weather_risk['risk_level']}")
    print()
    
    # 4. STREET CLOSURES
    print("4️⃣  STREET CLOSURES")
    print("-"*60)
    closures = get_closures.get_street_closures(start_lat, start_lng, radius_km=1.0, days_back=14)
    closure_impact = get_closures.assess_closure_impact(closures)
    print(f"✓ Total closures: {closures.get('total_closures', 0)}")
    print(f"✓ Impact: {closure_impact['impact']} - {closure_impact['message']}")
    print()
    
    # SUMMARY
    print("="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Routes generated: {len(routes)}")
    print(f"Safety analyzed: {len(enhanced_routes)} routes")
    print(f"Weather checked: {weather_risk['risk_level']} risk")
    print(f"Closures found: {closures.get('total_closures', 0)}")
    print()
    
    # Return all data
    return {
        "routes": routes,
        "safety_analysis": enhanced_routes,
        "weather": weather,
        "weather_risk": weather_risk,
        "closures": closures,
        "closure_impact": closure_impact
    }


if __name__ == "__main__":
    # Test location: Central Park
    test_lat = 40.7580
    test_lng = -73.9855
    target_distance = 5.0
    
    result = test_all_queries(test_lat, test_lng, target_distance)
    
    print("="*60)
    print("ALL QUERIES COMPLETE ✓")
    print("="*60)