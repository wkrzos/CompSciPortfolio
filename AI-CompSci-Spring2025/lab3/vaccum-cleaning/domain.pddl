(define (domain robot-cleaning)
  (:requirements :strips :typing :negative-preconditions)
  
  (:types
    robot - object
    room - object
  )
  
  (:predicates
    ;; Robot location
    (at ?r - robot ?p - room)
    
    ;; Room states
    (dirty ?p - room)
    (clean ?p - room)
    
    ;; Room connectivity
    (connected ?from ?to - room)
  )
  
  ;; Move robot between connected rooms
  (:action move
    :parameters (?r - robot ?from ?to - room)
    :precondition (and
      (at ?r ?from)
      (connected ?from ?to)
      (not (= ?from ?to))
    )
    :effect (and
      (at ?r ?to)
      (not (at ?r ?from))
    )
  )
  
  ;; Clean the current room
  (:action clean
    :parameters (?r - robot ?p - room)
    :precondition (and
      (at ?r ?p)
      (dirty ?p)
      (not (clean ?p))
    )
    :effect (and
      (clean ?p)
      (not (dirty ?p))
    )
  )
)
