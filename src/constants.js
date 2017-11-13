const row = 120,col=160
export var randCoordinates =[]
export var highWayCoordinates =[]
export var blkedCoordinates =[]
export var sfCells=Array(2).fill("")
var getRandomInt = function (min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min; //The maximum is exclusive and the minimum is inclusive
}
var gen_hard_cells=()=>{
    let counter=0;
    while(counter<8){
        randCoordinates.push([""])
        let xCor = getRandomInt(0,row)
        let yCor = getRandomInt(0,col)
        randCoordinates[counter][0]=xCor
        randCoordinates[counter][1]=yCor
        counter++
    }
}

var determine_direction=(direction,dirArray)=>{
    const dirConfig =[[2,3,4],[1,3,4],[1,2,4],[1,2,3]]
    if(dirArray.length===3)return 0
    if(dirArray.length===2){
      let diff = dirConfig[direction].filter(x => dirArray.indexOf(x) < 0 );
      return diff[0]
    }else{
      let diff = dirConfig[direction].filter(x => dirArray.indexOf(x) < 0 );
      return Math.random()<0.5?
       diff[0]:
       diff[1]
    }


}

var gen_hwy_cells=()=>{
    let xCor = getRandomInt(0,col)
    let yCor = getRandomInt(0,row)
    var startingCell
        ,nextDirection;
    var rand = Math.random()
    if(rand<=0.25){
        startingCell=[xCor,0]
        nextDirection=1// 1 : next move Down
    }
    else if(rand<=0.5){
        startingCell=[0,yCor]
        nextDirection=2// 2 : next move Right
    }
    else if(rand<=0.75){
        startingCell=[col-1,yCor]
        nextDirection=3// 3 : next move Left
    }
    else{
        startingCell=[xCor,row-1]
        nextDirection=4// 4:  next move Up
    }
    //console.log("prev length",highWayCoordinates.length)
    var prevLength = highWayCoordinates.length
    var collisionFlag=false
    var currentCell=startingCell
    highWayCoordinates.push(parseInt(currentCell[1],10)+","+parseInt(currentCell[0],10))
    var direction=[]
    var counter=0;
    do{

        counter++;
        if(counter>300) break;
        rand = Math.random()
        switch (nextDirection){
            case 1://prev Down
                    for(let i=0;i<20;i++){
                        if(highWayCoordinates.indexOf((parseInt(currentCell[1],10)+parseInt(i+1,10))+","+(parseInt(currentCell[0],10)))
                        !==-1){
                            // console.log("Down collision at ",(parseInt(currentCell[1],10)+parseInt(i+1,10))+","+(parseInt(currentCell[0],10)))
                            direction.push(nextDirection)
                            nextDirection=determine_direction(nextDirection-1,direction)
                            collisionFlag=true
                            break;
                        }
                    }
                    if(collisionFlag){
                      collisionFlag=false
                      break;
                    }
                    if(parseInt(currentCell[1],10)+20>= row-1){
                        if (row-1-parseInt(currentCell[1],10)+highWayCoordinates.length-prevLength>=100){
                            // console.log("near bound",row-1-parseInt(currentCell[1],10)+highWayCoordinates.length-prevLength)
                        for(let i=0;i<row-1-parseInt(currentCell[1],10);i++){
                            highWayCoordinates.push((parseInt(currentCell[1],10)+parseInt(i+1,10))+","+(parseInt(currentCell[0],10)))
                            }
                            // //console.log("Down hit bound",highWayCoordinates[highWayCoordinates.length-1])
                            return true;
                        }
                        direction.push(nextDirection)
                        nextDirection=determine_direction(nextDirection-1,direction)
                        break;
                    }
                    for(let i=0;i<20;i++){
                        highWayCoordinates.push((parseInt(currentCell[1],10)+parseInt(i+1,10))+","+(parseInt(currentCell[0],10)))
                    }
                    currentCell[1]=parseInt(currentCell[1],10)+20
                    if(rand<=0.2)//20% go Right
                    {
                        nextDirection = 2
                    }
                    else if(rand<=0.4){//20% go Left
                        nextDirection = 3
                    }
                    direction=[]
                    break;
            case 2://Right
                    for(let i=0;i<20;i++){
                        if(highWayCoordinates.indexOf(parseInt(currentCell[1],10)+","+(parseInt(currentCell[0],10)+parseInt(i+1,10)))
                        !==-1){
                            //console.log("Right collision at ",parseInt(currentCell[1],10)+","+(parseInt(currentCell[0],10)+parseInt(i+1,10)))
                            direction.push(nextDirection)
                            nextDirection=determine_direction(nextDirection-1,direction)
                            collisionFlag=true
                            break;
                        }
                    }
                    if(collisionFlag){
                      collisionFlag=false
                      break;
                    }
                    if(parseInt(currentCell[0],10)+20>= col-1){

                        if (col-1-parseInt(currentCell[0],10)+highWayCoordinates.length-prevLength>=100){
                            //console.log("near bound",col-1-parseInt(currentCell[0],10)+highWayCoordinates.length-prevLength)
                        for(let i=0;i<col-1-parseInt(currentCell[0],10);i++){
                            highWayCoordinates.push(parseInt(currentCell[1],10)+","+(parseInt(currentCell[0],10)+parseInt(i+1,10)))
                            }
                            //console.log("Right hit bound",highWayCoordinates[highWayCoordinates.length-1])
                            return true;
                        }
                        direction.push(nextDirection)
                        nextDirection=determine_direction(nextDirection-1,direction)
                        break;
                    }
                    for(let i=0;i<20;i++){
                        highWayCoordinates.push(parseInt(currentCell[1],10)+","+(parseInt(currentCell[0],10)+parseInt(i+1,10)))
                    }
                    currentCell[0]=parseInt(currentCell[0],10)+20
                    if(rand<=0.2)//20% go Down
                    {
                        nextDirection = 1
                    }
                    else if(rand<=0.4){//20% go Up
                        nextDirection = 4
                    }
                    direction=[]
                    break;
            case 3://Left
                    for(let i=0;i<20;i++){
                        if(highWayCoordinates.indexOf(parseInt(currentCell[1],10)+","+(parseInt(currentCell[0],10)-parseInt(i+1,10)))
                        !==-1){
                            //console.log("Left collision at ",parseInt(currentCell[1],10)+","+(parseInt(currentCell[0],10)-parseInt(i+1,10)))
                            direction.push(nextDirection)
                            nextDirection=determine_direction(nextDirection-1,direction)
                            collisionFlag=true
                            break;
                        }
                    }
                    if(collisionFlag){
                      collisionFlag=false
                      break;
                    }
                    if(parseInt(currentCell[0],10)-20<=0){
                        if (parseInt(currentCell[0],10)+highWayCoordinates.length-prevLength>=100){
                            //console.log("near bound",parseInt(currentCell[0],10)+highWayCoordinates.length-prevLength)
                        for(let i=0;i<parseInt(currentCell[0],10);i++){
                            highWayCoordinates.push(parseInt(currentCell[1],10)+","+(parseInt(currentCell[0],10)-parseInt(i+1,10)))
                            }
                            //console.log("Left hit bound",highWayCoordinates[highWayCoordinates.length-1])
                            return true ;
                        }
                        direction.push(nextDirection)
                        nextDirection=determine_direction(nextDirection-1,direction)
                        break;
                    }
                    for(let i=0;i<20;i++){
                        highWayCoordinates.push(parseInt(currentCell[1],10)+","+(parseInt(currentCell[0],10)-parseInt(i+1,10)))
                    }
                    currentCell[0]=parseInt(currentCell[0],10)-20
                    if(rand<=0.2)//20% go Down
                    {
                        nextDirection = 1
                    }
                    else if(rand<=0.4){//20% go Up
                        nextDirection = 4
                    }
                    direction=[]
                    break;
            case 4: //Up
                    for(let i=0;i<20;i++){
                        if(highWayCoordinates.indexOf((parseInt(currentCell[1],10)-parseInt(i+1,10))+","+(parseInt(currentCell[0],10)))
                        !==-1){
                            //console.log("Up collision at ",(parseInt(currentCell[1],10)-parseInt(i+1,10))+","+(parseInt(currentCell[0],10)))
                            direction.push(nextDirection)
                            nextDirection=determine_direction(nextDirection-1,direction)
                            collisionFlag=true
                            break;
                        }
                    }
                    if(collisionFlag){
                      collisionFlag=false
                      break;
                    }
                    if(parseInt(currentCell[1],10)-20<=0){
                        if (parseInt(currentCell[1],10)+highWayCoordinates.length-prevLength>=100){
                            //console.log("near bound",parseInt(currentCell[1],10)+highWayCoordinates.length-prevLength)
                        for(let i=0;i<parseInt(currentCell[1],10);i++){
                            highWayCoordinates.push((parseInt(currentCell[1],10)-parseInt(i+1,10))+","+parseInt(currentCell[0],10))
                            }
                            //console.log("Up hit bound",highWayCoordinates[highWayCoordinates.length-1])
                            return true;
                        }
                        direction.push(nextDirection)
                        nextDirection=determine_direction(nextDirection-1,direction)
                        break;
                    }
                    for(let i=0;i<20;i++){
                        highWayCoordinates.push((parseInt(currentCell[1],10)-parseInt(i+1,10))+","+(parseInt(currentCell[0],10)))
                    }
                    currentCell[1]=parseInt(currentCell[1],10)-20
                    if(rand<=0.2)//20% go Right
                    {
                        nextDirection = 2
                    }
                    else if(rand<=0.4){//20% go Left
                        nextDirection = 3
                    }
                    direction=[]
                    break;
            default:
                    highWayCoordinates=highWayCoordinates.slice(0,prevLength)
                    return false
                    break;

        }

    }while(parseInt(currentCell[0],10)!==0&&parseInt(currentCell[1],10)!==0&&parseInt(currentCell[0],10)!==col-1&&parseInt(currentCell[1],10)!==row-1)
    if(startingCell === currentCell) {
      highWayCoordinates=highWayCoordinates.slice(0,prevLength)
      return false//need redo whole process
    }
    return true
}

var gen_blocked_cells=()=>{
    let totalBLKCells = row*col/5
    for(let i =0;i<totalBLKCells;i++){
        let xCor = getRandomInt(0,col)
        let yCor = getRandomInt(0,row)
        let point = yCor+","+xCor
        if(highWayCoordinates.indexOf(point)===-1)
            if(blkedCoordinates.indexOf(point)===-1)
                blkedCoordinates.push(point)
            else
                i--
        else i--
    }
}
export var gen_start_final_cells=()=>{
    var flag
    for(let i=0;i<2;i++){
        flag=true
        if(Math.random()<0.5){//top or bottom 20 rows
            if(Math.random()<0.5){//top 20 rows
                while(flag){
                let xCor = getRandomInt(0,col)
                let yCor = getRandomInt(0,20)
                var point = yCor+","+xCor
                if(blkedCoordinates.indexOf(point)===-1)
                    flag=false;
                }
                sfCells[i] = point
            }else{//bottom 20 rows
                while(flag){
                let xCor = getRandomInt(0,col)
                let yCor = getRandomInt(row-20,row)
                var point = yCor+","+xCor
                if(blkedCoordinates.indexOf(point)===-1)
                    flag=false;
                }
                sfCells[i] = point
            }
        }else{//left or right 20 columns
            if(Math.random()<0.5){//left 20 cols
                while(flag){
                let xCor = getRandomInt(0,20)
                let yCor = getRandomInt(0,row)
                var point = yCor+","+xCor
                if(blkedCoordinates.indexOf(point)===-1)
                    flag=false;
                }
                sfCells[i] = point
            }else{//right 20 cols
                while(flag){
                let xCor = getRandomInt(col-20,col)
                let yCor = getRandomInt(0,row)
                var point = yCor+","+xCor
                if(blkedCoordinates.indexOf(point)===-1)
                    flag=false;
                }
                sfCells[i] = point
            }
        }

        if(i==1){
        let sx = sfCells[0].split(",")[0],
        sy = sfCells[0].split(",")[1],
        fx = sfCells[1].split(",")[0],
        fy = sfCells[1].split(",")[1]
        if(Math.abs(sx-fx)+Math.abs(sy-fy)<100){
            i=0//reselect the goal
            }
        }

    }

}


export var pathConfig =[]

var gen_path_config=()=>{
  var randC=0
  var hardTraverseCoordinates=[]
  var hardHwyCoordinates=[]
  var unblockedHwyCoordinates=[]
  let r,c
  for(r=0;r<row;r++){
      for(c=0;c<col;c++){
            let counter=0
            if(highWayCoordinates.indexOf(r+","+c)!==-1){
              unblockedHwyCoordinates.push(r+","+c)
            }
            while (counter<8){
              // console.log(r,point[0],c,point[1])
                if(r>=randCoordinates[counter][0]-15&&r<=randCoordinates[counter][0]+15&&
                  c>=randCoordinates[counter][1]-15&&c<=randCoordinates[counter][1]+15){
                  if(Math.random()<0.5){
                    hardTraverseCoordinates.push(r+","+c)
                    if(highWayCoordinates.indexOf(r+","+c)!==-1){
                        hardHwyCoordinates.push(r+","+c)
                      }
                    }
                    break
                  }
                  counter++
            }
          }
    }
    for(r=0;r<row;r++){
        pathConfig.push([])
      for(c=0;c<col;c++){
          if(blkedCoordinates.indexOf(r+","+c)!=-1)//blocked 0
                pathConfig[r].push(0)
          else if(hardTraverseCoordinates.indexOf(r+","+c)!=-1)//hard 2
          {
              if(hardHwyCoordinates.indexOf(r+","+c)!=-1)//hard hwy 2
                    pathConfig[r].push('b')
              else  pathConfig[r].push(2)
          }
          else if(unblockedHwyCoordinates.indexOf(r+","+c)!=-1)//hard 2
          {
                pathConfig[r].push('a')
          }
          else  pathConfig[r].push(1)
        }
    }

}

export var gen_everything=()=>{
    let flag = true,c=0
    while(flag){
      flag=false
      for(let i=0;i<4;i++){
          let result= gen_hwy_cells();
          if(result===false)i--
          c++
          if(c>20){
            flag=true
            break;
          };
      }
    }
    gen_blocked_cells()
    gen_start_final_cells()
    gen_path_config()
    console.log(sfCells)
}



gen_hard_cells();
