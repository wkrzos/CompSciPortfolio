(define (problem complex-multi-vehicle-transport)
  (:domain package-transport)
  (:requirements :strips :typing :negative-preconditions :conditional-effects)
  
  (:objects
    ;; Locations
    warsaw krakow gdansk wroclaw poznan - city
    warsaw-airport krakow-airport gdansk-airport - airport
    gdansk-port szczecin-port - port
    
    ;; Vehicles
    truck1 truck2 truck3 - truck
    plane1 plane2 - plane
    ship1 - ship
    
    ;; Packages
    package1 package2 package3 package4 package5 package6 - package
  )
  
  (:init
    ;; Initial vehicle locations
    (at truck1 warsaw)
    (at truck2 krakow)
    (at truck3 wroclaw)
    (at plane1 warsaw-airport)
    (at plane2 krakow-airport)
    (at ship1 gdansk-port)
    
    ;; Initial package locations
    (at package1 warsaw)
    (at package2 krakow)
    (at package3 gdansk)
    (at package4 wroclaw)
    (at package5 poznan)
    (at package6 warsaw)
    
    ;; Vehicle capabilities
    (can-drive truck1)
    (can-drive truck2)
    (can-drive truck3)
    (can-fly plane1)
    (can-fly plane2)
    (can-sail ship1)
    
    ;; Vehicle availability
    (available truck1)
    (available truck2)
    (available truck3)
    (available plane1)
    (available plane2)
    (available ship1)
    
    ;; Location types
    (is-city warsaw)
    (is-city krakow)
    (is-city gdansk)
    (is-city wroclaw)
    (is-city poznan)
    (is-airport warsaw-airport)
    (is-airport krakow-airport)
    (is-airport gdansk-airport)
    (is-port gdansk-port)
    (is-port szczecin-port)
    
    ;; Road connections (comprehensive network)
    (road-connected warsaw krakow)
    (road-connected krakow warsaw)
    (road-connected krakow gdansk)
    (road-connected gdansk krakow)
    (road-connected warsaw gdansk)
    (road-connected gdansk warsaw)
    (road-connected warsaw wroclaw)
    (road-connected wroclaw warsaw)
    (road-connected krakow wroclaw)
    (road-connected wroclaw krakow)
    (road-connected wroclaw poznan)
    (road-connected poznan wroclaw)
    (road-connected poznan gdansk)
    (road-connected gdansk poznan)
    (road-connected warsaw poznan)
    (road-connected poznan warsaw)
    
    ;; Airport connections to cities
    (road-connected warsaw warsaw-airport)
    (road-connected warsaw-airport warsaw)
    (road-connected krakow krakow-airport)
    (road-connected krakow-airport krakow)
    (road-connected gdansk gdansk-airport)
    (road-connected gdansk-airport gdansk)
    
    ;; Port connections
    (road-connected gdansk gdansk-port)
    (road-connected gdansk-port gdansk)
    
    ;; Air connections (all airports connected)
    (air-connected warsaw-airport krakow-airport)
    (air-connected krakow-airport warsaw-airport)
    (air-connected warsaw-airport gdansk-airport)
    (air-connected gdansk-airport warsaw-airport)
    (air-connected krakow-airport gdansk-airport)
    (air-connected gdansk-airport krakow-airport)
    
    ;; Water connections
    (water-connected gdansk-port szczecin-port)
    (water-connected szczecin-port gdansk-port)
    
    ;; Cost initialization
    (= (total-cost) 0)
    
    ;; Transport costs for trucks
    (= (transport-cost warsaw krakow truck1) 12)
    (= (transport-cost krakow warsaw truck1) 12)
    (= (transport-cost krakow gdansk truck1) 10)
    (= (transport-cost gdansk krakow truck1) 10)
    (= (transport-cost warsaw gdansk truck1) 18)
    (= (transport-cost gdansk warsaw truck1) 18)
    (= (transport-cost warsaw wroclaw truck1) 14)
    (= (transport-cost wroclaw warsaw truck1) 14)
    (= (transport-cost krakow wroclaw truck1) 8)
    (= (transport-cost wroclaw krakow truck1) 8)
    (= (transport-cost wroclaw poznan truck1) 6)
    (= (transport-cost poznan wroclaw truck1) 6)
    (= (transport-cost poznan gdansk truck1) 9)
    (= (transport-cost gdansk poznan truck1) 9)
    (= (transport-cost warsaw poznan truck1) 11)
    (= (transport-cost poznan warsaw truck1) 11)
    
    ;; Same costs for other trucks
    (= (transport-cost warsaw krakow truck2) 12)
    (= (transport-cost krakow warsaw truck2) 12)
    (= (transport-cost krakow gdansk truck2) 10)
    (= (transport-cost gdansk krakow truck2) 10)
    (= (transport-cost warsaw gdansk truck2) 18)
    (= (transport-cost gdansk warsaw truck2) 18)
    (= (transport-cost warsaw wroclaw truck2) 14)
    (= (transport-cost wroclaw warsaw truck2) 14)
    (= (transport-cost krakow wroclaw truck2) 8)
    (= (transport-cost wroclaw krakow truck2) 8)
    (= (transport-cost wroclaw poznan truck2) 6)
    (= (transport-cost poznan wroclaw truck2) 6)
    (= (transport-cost poznan gdansk truck2) 9)
    (= (transport-cost gdansk poznan truck2) 9)
    (= (transport-cost warsaw poznan truck2) 11)
    (= (transport-cost poznan warsaw truck2) 11)
    
    (= (transport-cost warsaw krakow truck3) 12)
    (= (transport-cost krakow warsaw truck3) 12)
    (= (transport-cost krakow gdansk truck3) 10)
    (= (transport-cost gdansk krakow truck3) 10)
    (= (transport-cost warsaw gdansk truck3) 18)
    (= (transport-cost gdansk warsaw truck3) 18)
    (= (transport-cost warsaw wroclaw truck3) 14)
    (= (transport-cost wroclaw warsaw truck3) 14)
    (= (transport-cost krakow wroclaw truck3) 8)
    (= (transport-cost wroclaw krakow truck3) 8)
    (= (transport-cost wroclaw poznan truck3) 6)
    (= (transport-cost poznan wroclaw truck3) 6)
    (= (transport-cost poznan gdansk truck3) 9)
    (= (transport-cost gdansk poznan truck3) 9)
    (= (transport-cost warsaw poznan truck3) 11)
    (= (transport-cost poznan warsaw truck3) 11)
    
    ;; Air transport costs (cheaper per distance but limited routes)
    (= (transport-cost warsaw-airport krakow-airport plane1) 6)
    (= (transport-cost krakow-airport warsaw-airport plane1) 6)
    (= (transport-cost warsaw-airport gdansk-airport plane1) 8)
    (= (transport-cost gdansk-airport warsaw-airport plane1) 8)
    (= (transport-cost krakow-airport gdansk-airport plane1) 7)
    (= (transport-cost gdansk-airport krakow-airport plane1) 7)
    
    (= (transport-cost warsaw-airport krakow-airport plane2) 6)
    (= (transport-cost krakow-airport warsaw-airport plane2) 6)
    (= (transport-cost warsaw-airport gdansk-airport plane2) 8)
    (= (transport-cost gdansk-airport warsaw-airport plane2) 8)
    (= (transport-cost krakow-airport gdansk-airport plane2) 7)
    (= (transport-cost gdansk-airport krakow-airport plane2) 7)
    
    ;; Water transport costs
    (= (transport-cost gdansk-port szczecin-port ship1) 15)
    (= (transport-cost szczecin-port gdansk-port ship1) 15)
    
    ;; Travel times
    (= (travel-time warsaw krakow truck1) 4)
    (= (travel-time krakow gdansk truck1) 3)
    (= (travel-time warsaw wroclaw truck1) 5)
    (= (travel-time wroclaw poznan truck1) 2)
    (= (travel-time poznan gdansk truck1) 3)
    
    (= (travel-time warsaw-airport krakow-airport plane1) 1)
    (= (travel-time krakow-airport gdansk-airport plane1) 1)
    (= (travel-time warsaw-airport gdansk-airport plane1) 2)
    
    ;; Loading times
    (= (loading-time package1 truck1) 1)
    (= (loading-time package2 truck2) 1)
    (= (loading-time package3 truck3) 1)
    (= (loading-time package4 truck1) 1)
    (= (loading-time package5 truck2) 1)
    (= (loading-time package6 truck3) 1)
  )
  
  (:goal
    (and
      ;; Complex delivery requirements
      (delivered package1)
      (at package1 gdansk)
      (delivered package2)
      (at package2 poznan)
      (delivered package3)
      (at package3 warsaw)
      (delivered package4)
      (at package4 krakow)
      (delivered package5)
      (at package5 gdansk)
      (delivered package6)
      (at package6 wroclaw)
    )
  )
  
  (:metric minimize (total-cost))
)
