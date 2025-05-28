(define (problem robot-cleaning-linear)
  (:domain robot-cleaning)
  (:requirements :strips :typing :negative-preconditions)
  
  (:objects
    robo - robot
    pokoj1 pokoj2 pokoj3 - room
  )
  
  (:init
    ;; Robot starts in the first room
    (at robo pokoj1)
    
    ;; All rooms are initially dirty
    (dirty pokoj1)
    (dirty pokoj2)
    (dirty pokoj3)
    
    ;; Linear connectivity: pokoj1 <-> pokoj2 <-> pokoj3
    (connected pokoj1 pokoj2)
    (connected pokoj2 pokoj1)
    (connected pokoj2 pokoj3)
    (connected pokoj3 pokoj2)
  )
  
  (:goal
    (and
      (clean pokoj1)
      (clean pokoj2)
      (clean pokoj3)
    )
  )
)
