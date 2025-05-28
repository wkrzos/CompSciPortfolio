(define (problem simple-transport)
  (:domain package-transport)
  (:requirements :strips :typing :negative-preconditions :conditional-effects)
  
  (:objects
    ;; Locations
    warsaw krakow gdansk - city
    warsaw-airport krakow-airport - airport
    gdansk-port - port
    
    ;; Vehicles
    truck1 truck2 - truck
    plane1 - plane
    ship1 - ship
    
    ;; Packages
    package1 package2 package3 - package
  )
  
  (:init
    ;; Initial vehicle locations
    (at truck1 warsaw)
    (at truck2 krakow)
    (at plane1 warsaw-airport)
    (at ship1 gdansk-port)
    
    ;; Initial package locations
    (at package1 warsaw)
    (at package2 krakow)
    (at package3 gdansk)
    
    ;; Vehicle capabilities
    (can-drive truck1)
    (can-drive truck2)
    (can-fly plane1)
    (can-sail ship1)
    
    ;; Vehicle availability
    (available truck1)
    (available truck2)
    (available plane1)
    (available ship1)
    
    ;; Location types
    (is-city warsaw)
    (is-city krakow)
    (is-city gdansk)
    (is-airport warsaw-airport)
    (is-airport krakow-airport)
    (is-port gdansk-port)
    
    ;; Road connections (bidirectional)
    (road-connected warsaw krakow)
    (road-connected krakow warsaw)
    (road-connected krakow gdansk)
    (road-connected gdansk krakow)
    (road-connected warsaw gdansk)
    (road-connected gdansk warsaw)
    
    ;; Airport connections to cities
    (road-connected warsaw warsaw-airport)
    (road-connected warsaw-airport warsaw)
    (road-connected krakow krakow-airport)
    (road-connected krakow-airport krakow)
    
    ;; Port connections
    (road-connected gdansk gdansk-port)
    (road-connected gdansk-port gdansk)
    
    ;; Air connections
    (air-connected warsaw-airport krakow-airport)
    (air-connected krakow-airport warsaw-airport)
    
    ;; Water connections (for demonstration)
    (water-connected gdansk-port gdansk-port)
  )
  
  (:goal
    (and
      (delivered package1)
      (at package1 krakow)
      (delivered package2)
      (at package2 gdansk)
      (delivered package3)
      (at package3 warsaw)
    )
  )
)
