import React from 'react';
import ReactDOM from 'react-dom';
import {Button,ToggleButtonGroup,ToggleButton} from 'react-bootstrap';
import './index.css';
import {randCoordinates,highWayCoordinates,blkedCoordinates,gen_four_hwy,sfCells,pathConfig} from './constants.js'


const BLOCKED_CELL = 0
const REG_UNBLOCKED_CELL = 1
const HARD_TRAVERSE_CELL = 2
const REG_UNBLOCKED_HWY_CELL = 'a'
const HARD_TRAVERSE_HWY_CELL = 'b'
const row = 120,col=160
gen_four_hwy();

  class Board extends React.PureComponent  {
    constructor(props) {
        super(props);
        this.state = {
            dataMatrix:Array(120).fill(Array(160).fill(0)),
        };
    }
    renderSquare(r,c,handleClick,cellType) {
      const colorGroup={'-1':'blue',0:'lightcoral',1:'white',2:'lightgrey','a':'white','b':'lightgrey'}
      const labelGroup={s:'S',f:'G'}
      return (
          <Button key={r+","+c} value={r+","+c+",gvalue-"+1} className="square" cursor="pointer" onClick={handleClick}
          style={{background:colorGroup[cellType]}}>
          {cellType==='a'&&<span class="separator"></span>}
          {cellType==='b'&&<span class="separator"></span>}
          {sfCells[0]===r+","+c&&<span style={{width:'100%',color:'black',fontSize:'15px'}}>S</span>}
          {sfCells[1]===r+","+c&&<span style={{width:'100%',color:'black',fontSize:'15px'}}>G</span>}
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
      console.log(pathConfig)
      //
      if(this.props.outputToggle){
        var FileSaver = require('file-saver');
        var blob = new Blob([partStr1], {type: "text/plain;charset=utf-8"});
        FileSaver.saveAs(blob, "partialString.txt");
      }
    }

    render() {
        let r,c
        var board =[]
        var rows =[]
        let cellType = REG_UNBLOCKED_CELL
        for(r=0;r<row;r++){
            for(c=0;c<col;c++){
              if(!this.props.inputToggle){
                    cellType=pathConfig[r][c]

                      //blue color center
                      // for(let cc in randCoordinates)
                      //   if(r===randCoordinates[cc][0]&&c===randCoordinates[cc][1])
                      //           cellType=-1
              }
              else{//take an input file

              }
             rows.push(this.renderSquare(r,c,this.handleClick,cellType))
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
        {board}
        </div>
      );
    }
  }

  class Game extends React.Component {
    constructor(){
      super()
      this.state={
        inputToggle:false,
        outputToggle:false,
      }

    }
    render() {
      return (
        <div>
        <Button>Uniform Cost</Button>
        <Button onClick={(e)=>this.setState({outputToggle:!this.state.outputToggle})}>File Output</Button>
        <Button onClick={(e)=>this.setState({inputToggle:!this.state.inputToggle})} >File Input</Button>
        <Board inputToggle={this.state.inputToggle}
        outputToggle={this.state.outputToggle}/>
        </div>

      );
    }
  }

  // ========================================

  ReactDOM.render(<Game />, document.getElementById("root"));
