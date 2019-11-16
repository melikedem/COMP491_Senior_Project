//Google Quick-draw Key: AIzaSyC1_soqtXV1mTyetVpJ4GglGD5RtXuFp4o
//https://quickdrawfiles.appspot.com/drawing/cat?&key=AIzaSyC1_soqtXV1mTyetVpJ4GglGD5RtXuFp4o&isAnimated={isAnimated}&format=JSON
const url1 = 'https://quickdrawfiles.appspot.com/drawing/'
const url2 = '?&key=AIzaSyC1_soqtXV1mTyetVpJ4GglGD5RtXuFp4o&isAnimated=false&format=JSON'


let obj;

let strokeIndex = 0;
let index = 0;
let cat;
let prevx, prevy;
let url; 
let pick;


function setup() {
  let thingname = JSON.parse(document.getElementById('json').textContent);
  let a = JSON.parse(thingname);
  obj = new DrawingObject(a.name, a.color, a.size, a.number, 300, 100, a.strokeArray);
  var canvas = createCanvas(1060,450);
  canvas.parent("sketchholder");
}



function draw() {
 //  alert(obj.strokeArray)
  obj.display()
}


class DrawingObject {
  constructor(name, color, size, number, location_X, location_Y, strokeArray) {
    this.ready= 0;
    this.name =name;
    this.color= color;
    this.size= size;
    this.number= number;
    this.index = 0;
    this.strokeIndex = 0;
    this.location_X = location_X;
    this.location_Y = location_Y;
    this.strokeArray = strokeArray;

  }


    display() {
//alert(this.strokeArray.length);
  for(let i=0; i <= this.strokeArray[this.strokeIndex][0].length; i++){
      let x = this.strokeArray[this.strokeIndex][0][this.index]+this.location_X ;
      let y = this.strokeArray[this.strokeIndex][1][this.index]+this.location_Y;
      stroke(this.color);
      if (this.prevx !== undefined) {
        line(this.prevx, this.prevy, x, y);
      }
      this.index++;
      if (this.index === this.strokeArray[this.strokeIndex][0].length) {
      this.strokeIndex++;
      this.prevx = undefined;
      this.prevy = undefined;
      this.index = 0;
      if (this.strokeIndex === this.strokeArray.length) {
        this.strokeArray = undefined;
        this.strokeIndex = 0;
      }
    } else {
      this.prevx = x;
      this.prevy = y;
    }
  }

  }
}