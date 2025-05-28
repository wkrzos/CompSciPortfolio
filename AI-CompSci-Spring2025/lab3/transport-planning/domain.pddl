(define (domain package-transport)
  (:requirements :strips :typing :negative-preconditions :conditional-effects)
  
  (:types
    location - object
    vehicle - object
    package - object
    truck - vehicle
    plane - vehicle
    ship - vehicle
    city - location
    airport - location
    port - location
    road-connection - object
    air-connection - object
    water-connection - object
  )
  
  (:predicates
    ;; Location predicates
    (at ?obj - object ?loc - location)
    (in ?pkg - package ?veh - vehicle)
    
    ;; Connection predicates
    (road-connected ?from ?to - location)
    (air-connected ?from ?to - location)
    (water-connected ?from ?to - location)
    
    ;; Vehicle capabilities
    (can-drive ?v - truck)
    (can-fly ?v - plane)
    (can-sail ?v - ship)
    
    ;; Vehicle availability
    (available ?v - vehicle)
    (busy ?v - vehicle)
    
    ;; Package status
    (delivered ?pkg - package)
    (picked-up ?pkg - package)
    
    ;; Location types
    (is-city ?loc - city)
    (is-airport ?loc - airport)
    (is-port ?loc - port)
  )

  ;; Load package into vehicle
  (:action load-package
    :parameters (?pkg - package ?veh - vehicle ?loc - location)
    :precondition (and 
      (at ?pkg ?loc)
      (at ?veh ?loc)
      (available ?veh)
      (not (picked-up ?pkg))
    )
    :effect (and
      (in ?pkg ?veh)
      (picked-up ?pkg)
      (not (at ?pkg ?loc))
    )
  )
  
  ;; Unload package from vehicle
  (:action unload-package
    :parameters (?pkg - package ?veh - vehicle ?loc - location)
    :precondition (and
      (in ?pkg ?veh)
      (at ?veh ?loc)
      (available ?veh)
    )
    :effect (and
      (at ?pkg ?loc)
      (not (in ?pkg ?veh))
    )
  )
  
  ;; Drive truck between road-connected locations
  (:action drive-truck
    :parameters (?truck - truck ?from ?to - location)
    :precondition (and
      (at ?truck ?from)
      (can-drive ?truck)
      (available ?truck)
      (road-connected ?from ?to)
      (not (= ?from ?to))
    )
    :effect (and
      (at ?truck ?to)
      (not (at ?truck ?from))
    )
  )
  
  ;; Fly plane between air-connected locations
  (:action fly-plane
    :parameters (?plane - plane ?from ?to - location)
    :precondition (and
      (at ?plane ?from)
      (can-fly ?plane)
      (available ?plane)
      (air-connected ?from ?to)
      (is-airport ?from)
      (is-airport ?to)
      (not (= ?from ?to))
    )
    :effect (and
      (at ?plane ?to)
      (not (at ?plane ?from))
    )
  )
  
  ;; Sail ship between water-connected locations
  (:action sail-ship
    :parameters (?ship - ship ?from ?to - location)
    :precondition (and
      (at ?ship ?from)
      (can-sail ?ship)
      (available ?ship)
      (water-connected ?from ?to)
      (is-port ?from)
      (is-port ?to)
      (not (= ?from ?to))
    )
    :effect (and
      (at ?ship ?to)
      (not (at ?ship ?from))
    )
  )
  
  ;; Deliver package (mark as delivered when at destination)
  (:action deliver-package
    :parameters (?pkg - package ?loc - location)
    :precondition (and
      (at ?pkg ?loc)
      (picked-up ?pkg)
      (not (delivered ?pkg))
    )
    :effect (and
      (delivered ?pkg)
    )
  )
  
  ;; Simplified multi-package loading action (without cost tracking)
  (:action load-multiple-packages
    :parameters (?veh - vehicle ?loc - location)
    :precondition (and
      (at ?veh ?loc)
      (available ?veh)
    )
    :effect (and
      ;; Conditional effects for different packages
      (forall (?pkg - package)
        (when (and (at ?pkg ?loc) (not (picked-up ?pkg)))
          (and (in ?pkg ?veh) (picked-up ?pkg) (not (at ?pkg ?loc)))
        )
      )
    )
  )
)
