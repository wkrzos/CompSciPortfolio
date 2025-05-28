(define (domain ball-moving-robot)
  (:requirements :strips :typing)
  
  (:types 
    robot room ball arm - object
  )
  
  (:predicates
    ;; Robot location
    (at ?r - robot ?rm - room)
    
    ;; Ball location  
    (inroom ?b - ball ?rm - room)
    
    ;; Arm states
    (holding ?a - arm ?b - ball)
    (arm-empty ?a - arm)
  )
  
  ;; Robot can move between rooms
  (:action move
    :parameters (?r - robot ?from - room ?to - room)
    :precondition (at ?r ?from)
    :effect (and (not (at ?r ?from)) 
                 (at ?r ?to))
  )
  
  ;; Robot can pick up a ball with an empty arm
  (:action pick-up
    :parameters (?r - robot ?a - arm ?b - ball ?rm - room)
    :precondition (and (at ?r ?rm) 
                       (inroom ?b ?rm) 
                       (arm-empty ?a))
    :effect (and (holding ?a ?b) 
                 (not (arm-empty ?a)) 
                 (not (inroom ?b ?rm)))
  )
  
  ;; Robot can put down a ball from its arm
  (:action put-down
    :parameters (?r - robot ?a - arm ?b - ball ?rm - room)
    :precondition (and (at ?r ?rm) 
                       (holding ?a ?b))
    :effect (and (inroom ?b ?rm) 
                 (arm-empty ?a) 
                 (not (holding ?a ?b)))
  )
)
