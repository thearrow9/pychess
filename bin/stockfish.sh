#!/bin/bash

(
echo "setoption name Hash value 64" ;
echo "setoption name Threads value 4" ;
echo "setoption name MultiPV value 1" ;
echo "setoption name Skill Level value $2" ;
echo "position fen $1" ;
echo "go movetime 1000" ;
sleep 2
) | engines/Stockfish/src/stockfish
