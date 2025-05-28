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
)
