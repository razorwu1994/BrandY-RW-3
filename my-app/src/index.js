import React from 'react';
import ReactDOM from 'react-dom';
import {Button} from 'react-bootstrap';
import './index.css';

  
  class Board extends React.Component {
    constructor() {
        super();
        this.state = {
            row:120,
            col:160,
            dataMatrix:Array(120).fill(Array(160).fill(0))
        };
    }
    renderSquare(r,c,handleClick) {
      return (
        <Button key={r+","+c} value={r+","+c} className="square" cursor="pointer" onClick={handleClick}>
        </Button>
      );
    }
    
    handleClick= (e)=>{
        console.log(e.target.value);
    }
    render() {
        // console.log(dataMatrix)
        let r,c
        var board =[]
        var rows =[]
        for(r=0;r<this.state.row;r++){
            for(c=0;c<this.state.col;c++){
             rows.push(this.renderSquare(r,c,this.handleClick))
            }
            board.push(
                <div className="board">
                    {rows}
                </div>
            )
            rows=[]
        }
        return (
        <div style={{overflowX:'visible',overflowY:'visible',width:'200%',height:'100%'}}>
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
              handleClick={i => this.handleClick(i)}
            />
      );
    }
  }
  
  // ========================================
  
  ReactDOM.render(<Game />, document.getElementById("root"));

  