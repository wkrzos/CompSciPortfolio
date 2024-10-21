(* Functional version of modified Pascal's triangle *)
let modifiedPascalF n =
  let rec elementWiseOperation a b op =
    match (a, b) with
    | [], _ -> b
    | _, [] -> a
    | x :: xs, y :: ys -> op x y :: elementWiseOperation xs ys op
  in

  let rec generateRow row =
    match row with
    | 0 -> [1]  (* Base case: Row 0 has a single element, which is 1. *)
    | _ ->
      let previousRow = generateRow (row - 1) in
      let operation =
        if row mod 2 = 0 then (+)  (* Addition for even rows *)
        else (-)  (* Subtraction for odd rows *)
      in
      (* Construct the current row by prepending 1 and performing element-wise operations. *)
      1 :: elementWiseOperation previousRow (List.tl previousRow) operation
  in

  (* Call the generateRow function to generate the desired row. *)
  generateRow n;;

(* Imperative version of modified Pascal's triangle *)
let modifiedPascalI n =
  if n = 0 then [1]
  else
    let currentRow = Array.make (n + 1) 0 in
    let previousRow = Array.make (n + 1) 0 in

    currentRow.(0) <- 1;
    previousRow.(0) <- 1;

    for rowIndex = 1 to n do
      if rowIndex mod 2 = 0 then (
        for columnIndex = 1 to rowIndex do
          currentRow.(columnIndex) <- previousRow.(columnIndex - 1) + previousRow.(columnIndex)
        done;
      )
      else (
        for columnIndex = 1 to rowIndex do
          previousRow.(columnIndex) <- currentRow.(columnIndex - 1) - currentRow.(columnIndex)
        done;
      )
    done;

    (* Check if n is even or odd and return the corresponding row as a list. *)
    if n mod 2 = 0 then Array.to_list currentRow
    else Array.to_list previousRow;;

(* Test cases *)
modifiedPascalF 0;;
modifiedPascalF 2;;
modifiedPascalF 3;;
modifiedPascalF 4;;
modifiedPascalF 5;;
modifiedPascalF 6;;

modifiedPascalI 0;;
modifiedPascalI 2;;
modifiedPascalI 3;;
modifiedPascalI 4;;
modifiedPascalI 5;;
modifiedPascalI 6;;
