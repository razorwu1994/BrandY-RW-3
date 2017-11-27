import React from 'react';
import ReactDOM from 'react-dom';
import {Button,DropdownButton,MenuItem} from 'react-bootstrap';
import './index.css';
import {randCoordinates,gen_everything,sfCells,pathConfig,gen_start_final_cells} from './constants.js'
import FileReaderInput from 'react-file-reader-input';
import ReactFileReader from 'react-file-reader'
import start from './start.png'
import goal from './goal.png'

const BLOCKED_CELL = 0
const REG_UNBLOCKED_CELL = 1
const HARD_TRAVERSE_CELL = 2
const REG_UNBLOCKED_HWY_CELL = 'a'
const HARD_TRAVERSE_HWY_CELL = 'b'
const row = 120,col=160
gen_everything();
var fileConfig = []
  class Board extends React.PureComponent  {
    constructor(props) {
        super(props);
        this.state = {
            dataMatrix:Array(120).fill(Array(160).fill(0)),
            genSFtoggle:false,
        };
    }
    renderSquare(r,c,handleClick,cellType,cellFGH) {
      const colorGroup={'-1':'blue',0:'lightcoral',1:'white',2:'lightgrey','a':'white','b':'lightgrey'}
      const labelGroup={s:'S',f:'G'}
      var storedval = r+","+c

      const hwydots = cellType==='a'||cellType==='b'?"separator":""
      const dotsConfig=[{text:"P",color:"#84DE02"},{text:"S",color:"blue"},{text:"G",color:"purple"}]
      const dot =  this.props.startANDgoal[0]===r+","+c?dotsConfig[1]:
                   this.props.startANDgoal[1]===r+","+c?dotsConfig[2]:
                   this.props.path.indexOf(storedval)!==-1?dotsConfig[0]:
                   ""
      const cellInfo = cellFGH.indexOf("[")!=-1?storedval+",g:[],h:[]"+cellFGH:storedval+",[f,g,h]:"+cellFGH
      return (
          <Button key={storedval} value={cellInfo} className="square" cursor="pointer" onClick={handleClick}
          style={{background:colorGroup[cellType]}}>

          <span id={cellInfo} value={cellInfo} style={{color:dot.color,width:'10px',fontSize:'15px'}}
            className={hwydots}>
          {dot.text}
          </span>
          </Button>
      );
    }



    computeHeuristic=(r,c,goal,mode)=>{
      // 1 heu_linear
      // 2 heu_manhatan
      // 3 heu_diagonal
      // 4 heu_eucliden
      // 5 heu_sample
      var i =0
      let xcor = goal.split(",")[0],ycor = goal.split(",")[1]
      switch(mode){
        case "1":
              i = Math.sqrt(Math.pow(r-xcor,2)+Math.pow(c-ycor,2))
              break
        case "2":
              i = Math.abs(r-xcor)+Math.abs(c-ycor)
              break
        case "3":
              i = Math.abs(r-xcor)+Math.abs(c-ycor)+(Math.sqrt(2)-2)*Math.min(Math.abs(r-xcor),Math.abs(c-ycor))* 1.01 //0.01 to break ties
              break
        case "4":
              i = Math.pow(r-xcor,2)+Math.pow(c-ycor,2)
              break
        case "5":
              let manhaX=Math.abs(r-xcor)
              let manhaY=Math.abs(c-ycor)
              i = Math.sqrt(2)*Math.min(manhaX,manhaY)+Math.max(manhaX,manhaY)-Math.min(manhaX,manhaY)
              break
        default:
              //console.log("invalid heuristic error")
              break
      }
      return i

    }
    genNewSF=()=>{
      this.setState({genSFtoggle:!this.state.genSFtoggle})
      this.props.updateSFcells()
    }

    handleClick= (e)=>{
        var location = e.target.value
        var info = document.getElementById("info")
        if(location!=undefined){
          var updateInfo = location
          info.innerHTML=updateInfo
          console.log(updateInfo)
        }
        else{
          info.innerHTML=e.target.id
          console.log(e.target)
        }


    }

    outputFile = ()=>{
      //sfCells,randCoordinates,hardTraverseCoordinates
      var config=[pathConfig,fileConfig]
      var index=0

      var partStr1 = sfCells[0]+"\n"+sfCells[1]+"\n"
      for(let temp in randCoordinates){
        if(temp === 7) {
          partStr1+=randCoordinates[temp]
        }
        else partStr1+=randCoordinates[temp]+"\n"
      }
      var partStr2
      if(this.props.inputToggle){
        index=1
      }
        partStr2 = config[index].reduce((a,b)=>{
        if(a.length===0){
            let temp=""
            for(let c =0;c<b.length;c++)
                temp+=b[c]
            return temp
        }
        else{
          let atemp=""
          for(let c =0;c<a.length;c++)
              atemp+=a[c]
          let btemp=""
          for(let c =0;c<b.length;c++)
                  btemp+=b[c]
          return atemp+"\n"+btemp
        }
      },""
      )
      //console.log(partStr2)
      //console.log(pathConfig)
      //
      if(this.props.outputToggle){
        var FileSaver = require('file-saver');
        var blob = new Blob([partStr1.trim()+"\n"+partStr2], {type: "text/plain;charset=utf-8"});
        FileSaver.saveAs(blob, "mapconfig.txt");

      }
      this.props.closeOutput
    }

    render() {
        let r,c
        var board =[]
        var rows =[]
        let cellType = REG_UNBLOCKED_CELL
        if(this.props.inputToggle){
          var tmp = this.props.fileConfig.split("\n").slice(10)
          fileConfig=[]
          for(let r=0;r<120;r++){
            fileConfig.push([])
            for(let c=0;c<160;c++){
              fileConfig[r].push(tmp[r].charAt(c))
            }
          }

        }
        var cellFGH=[]
        for(r=0;r<row;r++){
            for(c=0;c<col;c++){
              if(!this.props.inputToggle){
                    cellType=pathConfig[r][c]
                    cellFGH = this.props.cellFGH[r][c]
                    // heuristic = this.computeHeuristic(r,c,this.props.startANDgoal[1],this.props.heuristic)
                     // blue color center
                      // for(let cc in randCoordinates)
                      //   if(r===randCoordinates[cc][0]&&c===randCoordinates[cc][1])
                      //           cellType=-1
              }
              else{//take an input file
                  cellType=fileConfig[r][c]
                  cellFGH = this.props.cellFGH[r][c]
                  // heuristic = this.computeHeuristic(r,c,this.props.startANDgoal[1],this.props.heuristic)

              }
             rows.push(this.renderSquare(r,c,this.handleClick,cellType,cellFGH))
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
        <Button onClick={this.genNewSF} style={{backgroundColor:'purple',color:'white'}}>gen new start and goal</Button>
        Clicked Cell info :<span id="info"></span>
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
        config:"",
        startANDgoal:sfCells,
        blockedArray:[],
        heuristic:"5",
        searchMethod:'1',
        path:[],
        cellFGH:Array(120).fill(Array(160).fill([0,0,0])),
      }
    }

    changeHeuristic=(e)=>{
      this.setState({heuristic:e})
    }

    changeSearch=(e)=>{
      /*
      1:uniform_cost_search
      2:heuristic_search
      3:weighted_heuristic_search
      */
      console.log(e)
      this.setState({searchMethod:e})
    }

    uploadFile=(result)=>{
      var tmpResult = result.split("\n").slice(10)
      var tmp=[]
      for(let r=0;r<120;r++){
        for(let c=0;c<160;c++){
          if(tmpResult[r].charAt(c)==0)
            tmp.push(r+","+c)
        }
      }
      //console.log(tmp)
      this.setState({config:result,blockedArray:tmp})
    }
    updateSFcells=()=>{
      gen_start_final_cells(this.state.blockedArray)
      this.setState({startANDgoal:sfCells})
      console.log(sfCells)
    }

    handleChange = (files) => {
        if(files[0]  === null){
          this.setState({inputToggle:false})
          console.log("NULL file")
          return
        }
        var reader = new FileReader();
        reader.onload = (e) =>{
        // Use reader.result
        this.uploadFile(reader.result)
        }
        reader.readAsText(files[0]);
           setTimeout(()=>{
                    this.setState({inputToggle:true,startANDgoal:this.state.config.split("\n").slice(0,2)})
                    console.log(this.state.startANDgoal)
            }, 1000);
    }

    closeOutput=()=>{
      this.setState({outputToggle:false})
    }

    //only take file name with mapconfig.txt
    runScript=(files)=>{
      /*
      1:uniform_cost_search
      2:heuristic_search
      3:weighted_heuristic_search
      */
      let flag =files[0].name.startsWith("extra")?0:1 //0:cell,1:path
      let pathCopy=[]
      let cellFGHcopy=[]
      var reader = new FileReader();
      reader.onload = (e) =>{
      // Use reader.result
      if(flag===0){
        cellFGHcopy=JSON.parse(reader.result)
      }
      else
        pathCopy=JSON.parse(reader.result)
      }
      reader.readAsText(files[0]);
        setTimeout(()=>{
          if(flag===0){
          this.setState({cellFGH:cellFGHcopy})
          console.log(cellFGHcopy)
          }
          else {
            this.setState({path:pathCopy})
          }
          }, 1000);

    }

    render() {
      return (
        <div>
        <div style={{display:'flex'}}>
        <ReactFileReader handleFiles={this.runScript} fileTypes={'.txt'} >
        <Button bsStyle="info" cursor="pointer" style={{width:"100px"}}>Cell Info</Button>
        </ReactFileReader>
          <DropdownButton
          bsStyle="success" title={"Show heuristic"} id={`heuristic`} onSelect={this.changeHeuristic}>
          <MenuItem eventKey="1">h1 heu_euclidean</MenuItem>
          <MenuItem eventKey="2">h2 heu_manhatan</MenuItem>
          <MenuItem eventKey="3">h3(h1 in sequential,everything order going downwards) heu_diagonal</MenuItem>
          <MenuItem eventKey="4">h4 heu_euclidean_squared</MenuItem>
          <MenuItem eventKey="5">h5 heu_sample</MenuItem>
          </DropdownButton>
          <ReactFileReader handleFiles={this.runScript} fileTypes={'.txt'} >
              <Button bsStyle="danger" cursor="pointer" style={{width:"100px"}}>Show Path</Button>
          </ReactFileReader>
          <Button bsStyle="warning" onClick={(e)=>this.setState({outputToggle:!this.state.outputToggle})}>File Output</Button>
            <div style={{width:'90px'}}>
            <ReactFileReader handleFiles={this.handleChange} fileTypes={'.txt'} >
                <Button bsStyle="primary" cursor="pointer" style={{width:"100%"}}>Upload</Button>
            </ReactFileReader>
            </div>
        </div>

        <Board
        closeOutput={this.closeOutput}
        fileConfig={this.state.config}
        inputToggle={this.state.inputToggle}
        outputToggle={this.state.outputToggle}
        startANDgoal={this.state.startANDgoal}
        updateSFcells={this.updateSFcells}
        heuristic={this.state.heuristic}
        path={this.state.path}
        cellFGH={this.state.cellFGH}
        />
        </div>

      );
    }
  }

  // ========================================

  ReactDOM.render(<Game />, document.getElementById("root"));
