//Google Quick-draw Key: AIzaSyC1_soqtXV1mTyetVpJ4GglGD5RtXuFp4o
//https://quickdrawfiles.appspot.com/drawing/cat?&key=AIzaSyC1_soqtXV1mTyetVpJ4GglGD5RtXuFp4o&isAnimated={isAnimated}&format=JSON
const url1 = 'https://quickdrawfiles.appspot.com/drawing/'
const url2 = '?&key=AIzaSyC1_soqtXV1mTyetVpJ4GglGD5RtXuFp4o&isAnimated=false&format=JSON'

let thingname;
let drawingthing;

let strokeIndex = 0;
let index = 0;
let cat;
let prevx, prevy;
let url; 
let pick;

function setup() {
  var canvas = createCanvas(1060,450);
  canvas.parent("sketchholder");
  newDraw();
}

function pickathing(){
  thingname = JSON.parse(document.getElementById('object').textContent);
  pick = datatype[floor(random(344))];
  //thingname = JSON.stringify(url1+pick.join()+url2);
  //alert(typeof thingname); 
}
function newDraw() {
  //alert(thingname);
  //alert(typeof thingname);
  //let url = url1+thingname+url2;
  thingname = JSON.parse(document.getElementById('object').textContent);
  let url = url1+thingname+url2;
  console.log(url);
  loadJSON(url, gotDraw);
}

function gotDraw(data) {
  background(250);
  cat = data.drawing;
  //console.log(cat);
  
}


function draw() {
  if (cat) {
    let x = cat[strokeIndex][0][index];
    let y = cat[strokeIndex][1][index];
    line_color = color(0, 0, 255);
    stroke(line_color);
    //strokeWeight(3);
    if (prevx !== undefined) {
      line(prevx, prevy, x, y);
    }
    index++;
    if (index === cat[strokeIndex][0].length) {
      strokeIndex++;
      prevx = undefined;
      prevy = undefined;
      index = 0;
      if (strokeIndex === cat.length) {
        //console.log(strokeIndex);
        cat = undefined;
        strokeIndex = 0;
        //setTimeout(newCat, 250);
      }
    } else {
      prevx = x;
      prevy = y;
    }
  }
}


