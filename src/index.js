import React from 'react';
import ReactDOM from 'react-dom';
import {Button} from 'react-bootstrap';
import './index.css';
import {randCoordinates,highWayCoordinates,blkedCoordinates,gen_four_hwy,sfCells} from './constants.js'

var hardTraverseCoordinates=[]
var hardHwyCoordinates=[]
var unblockedHwyCoordinates=[]

const BLOCKED_CELL = 0
const REG_UNBLOCKED_CELL = 1
const HARD_TRAVERSE_CELL = 2
const REG_UNBLOCKED_HWY_CELL = 'a'
const HARD_TRAVERSE_HWY_CELL = 'b'
const START_CELL = 's'
const FINAL_CELL = 'f'
const row = 120,col=160
gen_four_hwy();

  class Board extends React.PureComponent  {
    constructor() {
        super();
        this.state = {
            dataMatrix:Array(120).fill(Array(160).fill(0)),
            info:"",            
        };
    }
    renderSquare(r,c,handleClick,cellType) { 
      const colorGroup={'-1':'blue',0:'lightcoral',1:'white',2:'lightgrey','a':'white','b':'lightgrey','s':'lightgreen','f':'lightgreen'}
      const labelGroup={s:'S',f:'G'}
      return ( 
          <Button key={r+","+c} value={r+","+c} className="square" cursor="pointer" onClick={handleClick}
          style={{background:colorGroup[cellType]}}>
          {cellType==='a'&&<span class="separator"></span>}
          {cellType==='b'&&<span class="separator"></span>}
          {cellType==='s'&&<span style={{width:'100%',color:'black',fontSize:'15px'}}>S</span>}
          {cellType==='f'&&<span style={{width:'100%',color:'black',fontSize:'15px'}}>G</span>}
          </Button>
      );
    }
    
    handleClick= (e)=>{
        let location = e.target.value,
            updateInfo = "The clicked cell is "+location
        console.log(updateInfo)
    }

    outputFile = ()=>{
      //sfCells,randCoordinates,hardTraverseCoordinates

      var partStr1 = sfCells[0]+"\n"+sfCells[1]+"\n"
      for(let temp in randCoordinates){
        partStr1+=randCoordinates[temp]+"\n"
      }
      console.log(partStr1)
      var partStr2=""
      var pathConfig =Array(row).fill(Array(col).fill(1))
      let r,c
      for(r=0;r<row;r++){
          for(c=0;c<col;c++){
            if(hardTraverseCoordinates.indexOf(r+","+c)!=-1)//hard 2
            {
                      pathConfig[r][c]=2
                if(hardHwyCoordinates.indexOf(r+","+c)!=-1)//hard 2
                      pathConfig[r][c]='b'
            }
            else if(unblockedHwyCoordinates.indexOf(r+","+c)!=-1)//hard 2
            {
                  pathConfig[r][c]='a'                  
            }
            else if(blkedCoordinates.indexOf(r+","+c)!=-1)//blocked 0
                  pathConfig[r][c]=0
          }
      }        
      console.log(hardTraverseCoordinates,hardHwyCoordinates,unblockedHwyCoordinates,blkedCoordinates)
      // console.log(highWayCoordinates)
      // console.log(blkedCoordinates)
      //console.log(hardTraverseCoordinates.length)
    }

    render() {
        let r,c
        var board =[]
        var rows =[]
        let cellType = REG_UNBLOCKED_CELL     
        for(r=0;r<row;r++){
            for(c=0;c<col;c++){
              let counter=0
              if(highWayCoordinates.indexOf(r+","+c)!==-1){
                cellType = REG_UNBLOCKED_HWY_CELL
                unblockedHwyCoordinates.push(r+","+c)
              }
              while (counter<8){
                // console.log(r,point[0],c,point[1])
                  if(r>=randCoordinates[counter][0]-31&&r<=randCoordinates[counter][0]+31&&
                    c>=randCoordinates[counter][1]-31&&c<=randCoordinates[counter][1]+31){
                    if(Math.random()<0.5){
                      hardTraverseCoordinates.push(r+","+c)
                      cellType = HARD_TRAVERSE_CELL                      
                      if(highWayCoordinates.indexOf(r+","+c)!==-1){
                          cellType = HARD_TRAVERSE_HWY_CELL                                            
                          hardHwyCoordinates.push(r+","+c)
                        }
                      }
                      break
                    }
                    counter++
              }
              if(blkedCoordinates.indexOf(r+","+c)!==-1)cellType=BLOCKED_CELL 
              if(sfCells.indexOf(r+","+c)===0)cellType=START_CELL
              if(sfCells.indexOf(r+","+c)===1)cellType=FINAL_CELL
              // for(let cc in randCoordinates)  
              //   if(r===randCoordinates[cc][0]&&c===randCoordinates[cc][1])
              //           cellType=-1 
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
        this.outputFile()
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

  