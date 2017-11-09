import React from 'react';
import ReactDOM from 'react-dom';
import {Button} from 'react-bootstrap';
import './index.css';
import {randCoordinates} from './constants.js'
const BLOCKED_CELL = 0
const REG_UNBLOCKED_CELL = 1
const HARD_TRAVERSE_CELL = 2
const REG_UNBLOCKED_HWY_CELL = 'a'
const HARD_TRAVERSE_HWY_CELL = 'b'
const row = 120,col=160
// var randCoordinates =[]
// var getRandomInt = function (min, max) {
//   min = Math.ceil(min);
//   max = Math.floor(max);
//   return Math.floor(Math.random() * (max - min)) + min; //The maximum is exclusive and the minimum is inclusive
// }
// var gen_hard_cells=()=>{
//     let counter=0;
//     while(counter<8){
//         randCoordinates.push([""])
//         let xCor = getRandomInt(0,row)
//         let yCor = getRandomInt(0,col)
//         randCoordinates[counter][0]=xCor
//         randCoordinates[counter][1]=yCor
//         counter++
//     }
// }
// gen_hard_cells();

  class Board extends React.PureComponent  {
    constructor() {
        super();
        this.state = {
            dataMatrix:Array(120).fill(Array(160).fill(0)),
            info:"",            
        };
    }
    renderSquare(r,c,handleClick,cellType) {
      const colorGroup={0:'lightcoral',1:'white',2:'lightgrey'}
      return ( 
          <Button key={r+","+c} value={r+","+c} className="square" cursor="pointer" onClick={handleClick}
          style={{background:colorGroup[cellType]}}>
          </Button>
      );
    }
    
    handleClick= (e)=>{
        let location = e.target.value,
            updateInfo = "The clicked cell is "+location
        console.log(updateInfo)
    }
    render() {
        let r,c
        var board =[]
        var rows =[]
        let cellType = REG_UNBLOCKED_CELL
        for(r=0;r<row;r++){
            for(c=0;c<col;c++){
              let counter=0
              while (counter<8){
                // console.log(r,point[0],c,point[1])
                  if(r>=randCoordinates[counter][0]-31&&r<=randCoordinates[counter][0]+31&&
                    c>=randCoordinates[counter][1]-31&&c<=randCoordinates[counter][1]+31){
                    if(Math.random()>=0.5)
                      cellType = HARD_TRAVERSE_CELL
                    break
                    }
                    counter++
              }
             rows.push(this.renderSquare(r,c,this.handleClick,cellType))
             cellType = REG_UNBLOCKED_CELL
            }
            board.push(
                <div className="board">
                    {rows}
                </div>
            )
            rows=[]
        }
        return (
        <div style={{overflowX:'visible',overflowY:'visible',width:'200%',height:'150%'}}>
        <div style={{width:'50%',height:'30%',fontSize:'20px',color:'black'}}>
          {this.state.info}
        </div>
        {board}   
        </div>
      );
    }
  }
  
  class Game extends React.Component {
    render() {
      return (
            <Board
              //squares={current.squares}
            />
      );
    }
  }
  
  // ========================================
  
  ReactDOM.render(<Game />, document.getElementById("root"));

  