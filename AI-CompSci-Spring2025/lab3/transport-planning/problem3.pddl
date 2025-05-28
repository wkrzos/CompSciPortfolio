(define (problem multi-modal-transport)
  (:domain package-transport)
  (:requirements :strips :typing :negative-preconditions :conditional-effects)
  
  (:objects
    ;; Cities
    warsaw krakow gdansk wroclaw szczecin hamburg berlin - city
    
    ;; Airports  
    warsaw-airport krakow-airport gdansk-airport berlin-airport hamburg-airport - airport
    
    ;; Ports
    gdansk-port szczecin-port hamburg-port - port
    
    ;; Vehicles
    truck1 truck2 truck3 - truck
    plane1 plane2 - plane
    ship1 ship2 - ship
    
    ;; Packages with different priorities
    urgent-package1 urgent-package2 - package
    regular-package1 regular-package2 regular-package3 - package
    bulk-package1 bulk-package2 - package
  )
  
  (:init
    ;; Initial vehicle locations
    (at truck1 warsaw)
    (at truck2 gdansk)
    (at truck3 wroclaw)
    (at plane1 warsaw-airport)
    (at plane2 berlin-airport)
    (at ship1 gdansk-port)
    (at ship2 hamburg-port)
    
    ;; Initial package locations
    (at urgent-package1 warsaw)
    (at urgent-package2 krakow)
    (at regular-package1 gdansk)
    (at regular-package2 wroclaw)
    (at regular-package3 szczecin)
    (at bulk-package1 gdansk)
    (at bulk-package2 hamburg)
    
    ;; Vehicle capabilities
    (can-drive truck1)
    (can-drive truck2)
    (can-drive truck3)
    (can-fly plane1)
    (can-fly plane2)
    (can-sail ship1)
    (can-sail ship2)
    
    ;; Vehicle availability
    (available truck1)
    (available truck2)
    (available truck3)
    (available plane1)
    (available plane2)
    (available ship1)
    (available ship2)
    
    ;; Location types
    (is-city warsaw)
    (is-city krakow)
    (is-city gdansk)
    (is-city wroclaw)
    (is-city szczecin)
    (is-city hamburg)
    (is-city berlin)
    (is-airport warsaw-airport)
    (is-airport krakow-airport)
    (is-airport gdansk-airport)
    (is-airport berlin-airport)
    (is-airport hamburg-airport)
    (is-port gdansk-port)
    (is-port szczecin-port)
    (is-port hamburg-port)
    
    ;; Road connections (Poland network)
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
    (road-connected gdansk szczecin)
    (road-connected szczecin gdansk)
    (road-connected wroclaw berlin)
    (road-connected berlin wroclaw)
    (road-connected berlin hamburg)
    (road-connected hamburg berlin)
    
    ;; Airport connections to cities
    (road-connected warsaw warsaw-airport)
    (road-connected warsaw-airport warsaw)
    (road-connected krakow krakow-airport)
    (road-connected krakow-airport krakow)
    (road-connected gdansk gdansk-airport)
    (road-connected gdansk-airport gdansk)
    (road-connected berlin berlin-airport)
    (road-connected berlin-airport berlin)
    (road-connected hamburg hamburg-airport)
    (road-connected hamburg-airport hamburg)
    
    ;; Port connections
    (road-connected gdansk gdansk-port)
    (road-connected gdansk-port gdansk)
    (road-connected szczecin szczecin-port)
    (road-connected szczecin-port szczecin)
    (road-connected hamburg hamburg-port)
    (road-connected hamburg-port hamburg)
    
    ;; International air connections
    (air-connected warsaw-airport berlin-airport)
    (air-connected berlin-airport warsaw-airport)
    (air-connected warsaw-airport hamburg-airport)
    (air-connected hamburg-airport warsaw-airport)
    (air-connected krakow-airport berlin-airport)
    (air-connected berlin-airport krakow-airport)
    (air-connected gdansk-airport hamburg-airport)
    (air-connected hamburg-airport gdansk-airport)
    (air-connected berlin-airport hamburg-airport)
    (air-connected hamburg-airport berlin-airport)
    
    ;; Water connections (Baltic Sea)
    (water-connected gdansk-port szczecin-port)
    (water-connected szczecin-port gdansk-port)
    (water-connected gdansk-port hamburg-port)
    (water-connected hamburg-port gdansk-port)
    (water-connected szczecin-port hamburg-port)
    (water-connected hamburg-port szczecin-port)
    
    ;; Road transport costs (higher for international routes)
    (= (transport-cost warsaw krakow truck1) 15)
    (= (transport-cost krakow warsaw truck1) 15)
    (= (transport-cost warsaw gdansk truck1) 20)
    (= (transport-cost gdansk warsaw truck1) 20)
    (= (transport-cost gdansk szczecin truck1) 12)
    (= (transport-cost szczecin gdansk truck1) 12)
    (= (transport-cost wroclaw berlin truck1) 25)
    (= (transport-cost berlin wroclaw truck1) 25)
    (= (transport-cost berlin hamburg truck1) 18)
    (= (transport-cost hamburg berlin truck1) 18)
    
    ;; Same costs for other trucks
    (= (transport-cost warsaw krakow truck2) 15)
    (= (transport-cost krakow warsaw truck2) 15)
    (= (transport-cost warsaw gdansk truck2) 20)
    (= (transport-cost gdansk warsaw truck2) 20)
    (= (transport-cost gdansk szczecin truck2) 12)
    (= (transport-cost szczecin gdansk truck2) 12)
    (= (transport-cost wroclaw berlin truck2) 25)
    (= (transport-cost berlin wroclaw truck2) 25)
    (= (transport-cost berlin hamburg truck2) 18)
    (= (transport-cost hamburg berlin truck2) 18)
    
    (= (transport-cost warsaw krakow truck3) 15)
    (= (transport-cost krakow warsaw truck3) 15)
    (= (transport-cost warsaw gdansk truck3) 20)
    (= (transport-cost gdansk warsaw truck3) 20)
    (= (transport-cost gdansk szczecin truck3) 12)
    (= (transport-cost szczecin gdansk truck3) 12)
    (= (transport-cost wroclaw berlin truck3) 25)
    (= (transport-cost berlin wroclaw truck3) 25)
    (= (transport-cost berlin hamburg truck3) 18)
    (= (transport-cost hamburg berlin truck3) 18)
    
    ;; Air transport costs (fast but expensive)
    (= (transport-cost warsaw-airport berlin-airport plane1) 30)
    (= (transport-cost berlin-airport warsaw-airport plane1) 30)
    (= (transport-cost warsaw-airport hamburg-airport plane1) 35)
    (= (transport-cost hamburg-airport warsaw-airport plane1) 35)
    (= (transport-cost krakow-airport berlin-airport plane1) 28)
    (= (transport-cost berlin-airport krakow-airport plane1) 28)
    (= (transport-cost gdansk-airport hamburg-airport plane1) 25)
    (= (transport-cost hamburg-airport gdansk-airport plane1) 25)
    (= (transport-cost berlin-airport hamburg-airport plane1) 20)
    (= (transport-cost hamburg-airport berlin-airport plane1) 20)
    
    (= (transport-cost warsaw-airport berlin-airport plane2) 30)
    (= (transport-cost berlin-airport warsaw-airport plane2) 30)
    (= (transport-cost warsaw-airport hamburg-airport plane2) 35)
    (= (transport-cost hamburg-airport warsaw-airport plane2) 35)
    (= (transport-cost krakow-airport berlin-airport plane2) 28)
    (= (transport-cost berlin-airport krakow-airport plane2) 28)
    (= (transport-cost gdansk-airport hamburg-airport plane2) 25)
    (= (transport-cost hamburg-airport gdansk-airport plane2) 25)
    (= (transport-cost berlin-airport hamburg-airport plane2) 20)
    (= (transport-cost hamburg-airport berlin-airport plane2) 20)
    
    ;; Water transport costs (slow but cheap for bulk)
    (= (transport-cost gdansk-port szczecin-port ship1) 8)
    (= (transport-cost szczecin-port gdansk-port ship1) 8)
    (= (transport-cost gdansk-port hamburg-port ship1) 15)
    (= (transport-cost hamburg-port gdansk-port ship1) 15)
    (= (transport-cost szczecin-port hamburg-port ship1) 12)
    (= (transport-cost hamburg-port szczecin-port ship1) 12)
    
    (= (transport-cost gdansk-port szczecin-port ship2) 8)
    (= (transport-cost szczecin-port gdansk-port ship2) 8)
    (= (transport-cost gdansk-port hamburg-port ship2) 15)
    (= (transport-cost hamburg-port gdansk-port ship2) 15)
    (= (transport-cost szczecin-port hamburg-port ship2) 12)
    (= (transport-cost hamburg-port szczecin-port ship2) 12)
    
    ;; Travel times (reflecting transport mode characteristics)
    (= (travel-time warsaw krakow truck1) 5)
    (= (travel-time warsaw gdansk truck1) 7)
    (= (travel-time gdansk szczecin truck1) 4)
    (= (travel-time wroclaw berlin truck1) 8)
    (= (travel-time berlin hamburg truck1) 6)
    
    ;; Air travel is fast
    (= (travel-time warsaw-airport berlin-airport plane1) 2)
    (= (travel-time warsaw-airport hamburg-airport plane1) 3)
    (= (travel-time krakow-airport berlin-airport plane1) 2)
    (= (travel-time gdansk-airport hamburg-airport plane1) 2)
    (= (travel-time berlin-airport hamburg-airport plane1) 1)
    
    ;; Sea travel is slow
    (= (travel-time gdansk-port szczecin-port ship1) 6)
    (= (travel-time gdansk-port hamburg-port ship1) 12)
    (= (travel-time szczecin-port hamburg-port ship1) 10)
    
    ;; Loading times
    (= (loading-time urgent-package1 truck1) 1)
    (= (loading-time urgent-package2 truck2) 1)
    (= (loading-time regular-package1 truck1) 2)
    (= (loading-time regular-package2 truck2) 2)
    (= (loading-time regular-package3 truck3) 2)
    (= (loading-time bulk-package1 ship1) 4)
    (= (loading-time bulk-package2 ship2) 4)
  )

  (:goal
    (and
      ;; Urgent packages need fast delivery
      (delivered urgent-package1)
      (at urgent-package1 berlin)
      (delivered urgent-package2)
      (at urgent-package2 hamburg)
      
      ;; Regular packages
      (delivered regular-package1)
      (at regular-package1 warsaw)
      (delivered regular-package2)
      (at regular-package2 hamburg)
      (delivered regular-package3)
      (at regular-package3 krakow)
      
      ;; Bulk packages (cost-sensitive)
      (delivered bulk-package1)
      (at bulk-package1 hamburg)
      (delivered bulk-package2)
      (at bulk-package2 gdansk)
    )
  )
)
