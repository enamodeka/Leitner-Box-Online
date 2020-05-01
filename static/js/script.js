/**
 * UI VARIABLES
 */
const ui_btn_add_to_deck = document.querySelector("#ui_btn_add_to_deck");
const ui_btn_update_card = document.querySelector("#ui_btn_update_card");
const ui_btn_flip = document.querySelector("#ui_btn_flip");
const ui_card_front = document.querySelector("#ui_card_front");
const ui_card_back = document.querySelector("#ui_card_back");
const ui_text_front = document.querySelector("#ui_text_front");
const ui_text_back = document.querySelector("#ui_text_back");
const ui_btn_right = document.querySelector(".card__button--right");
const ui_btn_wrong = document.querySelector(".card__button--wrong");
const ui_btn_upload = document.querySelector("#ui_btn_upload");
const ui_input_file= document.querySelector("#input-file");
const ui_card = document.querySelector("#ui_card");
const ui_image_front = document.querySelector("#ui_image_front");
const ui_image_back = document.querySelector("#ui_image_back");

/*****************
 * STATE VARIABLES
 *****************/
let card_flip = false;

let image_front_url = '';
let image_front_scale = 100;
let image_front_xPos = 0;
let image_front_yPos = 0;

let image_back_url = '';
let image_back_scale = 100;
let image_back_xPos = 0;
let image_back_yPos = 0;

/**
 * LISTENERS
 */

 /**
  * TOGGLE CARD FACE / ANSWER BUTTONS
  */
if (ui_btn_flip != null) {
  ui_btn_flip.addEventListener("click", function (e) {
    console.log("Click");
    e.preventDefault();
    // show right.wrong buttons
    if (ui_btn_right != null && ui_btn_wrong != null) {
      ui_btn_right.style.cssText = "display: block";
      ui_btn_wrong.style.cssText = "display: block";
    }
    if (!card_flip) {
      ui_card_front.classList.add("card__front--flip");
      ui_card_back.classList.add("card__back--flip");
      ui_card_front.classList.add("card__front--hide");
      ui_card_back.classList.add("card__back--show");
      
      card_flip = true;
    } else {
      ui_card_back.classList.remove("card__back--flip");
      ui_card_front.classList.remove("card__front--flip");
      ui_card_front.classList.remove("card__front--hide");
      ui_card_back.classList.remove("card__back--show");
      
      card_flip = false;
    }
  });
}

if (ui_input_file != null) {
ui_input_file.addEventListener('change', function() {
  uploadFile();
})

}

// ADD NEW CARD
if (ui_btn_add_to_deck != null) {
  ui_btn_add_to_deck.addEventListener("click", function (e) {
    e.preventDefault();
    console.log(
      "Unescaped front text:",
      ui_text_front.innerHTML.replace(/\s+/g, " ")
    );
    const data = {
      text_front: ui_text_front.innerHTML.replace(/\s+/g, " "),
      text_back: ui_text_back.innerHTML.replace(/\s+/g, " "),
      image_front_url: image_front_url,
      image_back_url: image_back_url,
      image_front_config: {
        image_front_scale,
        image_front_xPos,
        image_front_yPos
      },
      image_back_config: {
        image_back_scale,
        image_back_xPos,
        image_back_yPos
      }
    };
    console.log("Data ready to stringify", data);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/add-card");
    xhr.setRequestHeader("Content-type", "application/json");
    const dataToSend = JSON.stringify(data);
    console.log("Data to send", dataToSend);
    xhr.send(dataToSend);
    xhr.onload = function () {
      if (xhr.status === 200) {
        console.log("Response sunccessful");
        window.location.href = "/card-added";
      }
    };
  });
}

if (ui_btn_update_card != null) {
  ui_btn_update_card.addEventListener("click", function (e) {
    e.preventDefault();
    card_id = this.getAttribute("card_id");
    alert("Card saved.");
    console.log(
      "Unescaped front text:",
      ui_text_front.innerHTML.replace(/\s+/g, " ")
    );
    const data = {
      card_id: card_id,
      text_front: ui_text_front.innerHTML.replace(/\s+/g, " "),
      text_back: ui_text_back.innerHTML.replace(/\s+/g, " "),
      image_front_url: image_front_url,
      image_back_url: image_back_url,
      image_front_config: {
        image_front_scale,
        image_front_xPos,
        image_front_yPos
      },
      image_back_config: {
        image_back_scale,
        image_back_xPos,
        image_back_yPos
      }
    };
    console.log("Data ready to stringify", data);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/update-card");
    xhr.setRequestHeader("Content-type", "application/json");
    const dataToSend = JSON.stringify(data);
    console.log("Data to send", dataToSend);
    xhr.send(dataToSend);
    xhr.onload = function () {
      if (xhr.status === 200) {
        console.log("Response sunccessful. Card updated.");
        // window.location.href = '/card-added';
      }
    };
  });
}

function uploadFile() {
  console.log('uplaod func')
  let photo = document.getElementById("input-file").files[0];
    let form = document.getElementById("form");
    let data = new FormData(form);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload/image");
    xhr.send(data);
    xhr.onload = () => {
      if (xhr.status === 200) {
        if (!card_flip) {
          setImage(xhr.responseText, "front");
        } else {
          setImage(xhr.responseText, "back");
        }
      }
    };
}

if (ui_btn_upload != null) {
  ui_btn_upload.addEventListener("click", (e) => {
    e.preventDefault();
    ui_input_file.click();
  });
}

const setImage = (url, side) => {
  if (side == "front") {
    image_front_url = url;
    let scale = 100;
    ui_image_front.style.backgroundImage = "url('" + url + "')";
    ui_image_front.style.backgroundSize = scale + "%";
    ui_card_front.addEventListener("wheel", (e) => {
      scale = scale + e.deltaY;
      ui_image_front.style.backgroundSize = scale + "%";
      image_front_scale = scale;
    });
  } else {
    image_back_url = url;
    let scale = 100;
    ui_image_back.style.backgroundImage = "url('" + url + "')";
    ui_image_back.style.backgroundSize = scale + "%";
    ui_card_back.addEventListener("wheel", (e) => {
      scale = scale + e.deltaY;
      ui_image_back.style.backgroundSize = scale + "%";
      image_back_scale = scale;
    });
  }
};

/**
 * Load Card Config from DB
 */

 function loadCardFromDB(card_data) {
  console.log(card_data);
  image_front_url = card_data['image_front_url'];
  image_front_scale = card_data['image_front_config']['image_front_scale'];
  image_front_xPos = card_data['image_front_config']['image_front_xPos'];
  image_front_yPos = card_data['image_front_config']['image_front_yPos'];

  image_back_url = card_data['image_back_url'];
  image_back_scale = card_data['image_back_config']['image_back_scale'];
  image_back_xPos = card_data['image_back_config']['image_back_xPos'];;
  image_back_yPos = card_data['image_back_config']['image_back_yPos'];

  setImage(image_front_url, 'front');
  setImage(image_back_url, 'back');

  ui_image_front.style.backgroundSize = image_front_scale + "%";
  ui_image_back.style.backgroundSize = image_back_scale + "%";

  setTranslate(image_front_xPos, image_front_yPos, ui_image_front);
  setTranslate(image_back_xPos, image_back_yPos, ui_image_back);
 }

/**
 *
 * DRAG IMAGE
 */

let active = false;
let currentX,
  currentY,
  initialX_front,
  initialY_front,
  initialX_back,
  initialY_back,
  xOffset_front = 0,
  yOffset_front = 0,
  xOffset_back = 0,
  yOffset_back = 0;

const dragStart = (e) => {
  let xOffset, yOffset;

  if (!card_flip) {
    xOffset = xOffset_front;
    yOffset = yOffset_front;
  } else {
    xOffset = xOffset_back;
    yOffset = yOffset_back;
  }

  let initialX, initialY;
  console.log("drag start", e);
  if (e.type === "touchstart") {
    initialX = e.touches[0].clientX - xOffset;
    initialY = e.touches[0].clientY - yOffset;
  } else {
    initialX = e.clientX - xOffset;
    initialY = e.clientY - yOffset;
  }

  if (!card_flip) {
    initialX_front = initialX;
    initialY_front = initialY;
  } else {
    initialX_back = initialX;
    initialY_back = initialY;
  }

  let target = !card_flip ? ui_image_front : ui_image_back;
  console.log("Target: ", target);

  if (e.target === target) {
    console.log("Target check ok.");
    active = true;
  }
};

function dragEnd(e) {
  // initialX = currentX;
  // initialY = currentY;

  if (!card_flip) {
    initialX_front = currentX;
    initialY_front = currentY;
  } else {
    initialX_back = currentX;
    initialY_back = currentY;
  }

  active = false;
}

function drag(e) {
  if (active) {
    e.preventDefault();

    let initialX, initialY;
    if (!card_flip) {
      initialX = initialX_front;
      initialY = initialY_front;
    } else {
      initialX = initialX_back;
      initialY = initialY_back;
    }

    if (e.type === "touchmove") {
      currentX = e.touches[0].clientX - initialX;
      currentY = e.touches[0].clientY - initialY;
    } else {
      currentX = e.clientX - initialX;
      currentY = e.clientY - initialY;
    }

    if (!card_flip) {
      xOffset_front = currentX;
      yOffset_front = currentY;
    } else {
      xOffset_back = currentX;
      yOffset_back = currentY;
    }

    if (!card_flip) {
      setTranslate(currentX, currentY, ui_image_front);
      image_front_xPos = currentX;
      image_front_yPos = currentY;
    } else {
      setTranslate(currentX, currentY, ui_image_back);
      image_back_xPos = currentX;
      image_back_yPos = currentY;
    }
  }
}

function setTranslate(xPos, yPos, el) {
  // console.log('el', el);
  // el.style.transform = "translate3d(" + xPos + "px, " + yPos + "px, 0)";
  el.style.backgroundPosition = " " + xPos + "px " + yPos + "px";
}

ui_card_front.addEventListener("touchstart", dragStart, false);
ui_card_front.addEventListener("touchend", dragEnd, false);
ui_card_front.addEventListener("touchmove", drag, false);

ui_card_front.addEventListener("mousedown", dragStart, false);
ui_card_front.addEventListener("mouseup", dragEnd, false);
ui_card_front.addEventListener("mousemove", drag, false);

ui_card_back.addEventListener("touchstart", dragStart, false);
ui_card_back.addEventListener("touchend", dragEnd, false);
ui_card_back.addEventListener("touchmove", drag, false);

ui_card_back.addEventListener("mousedown", dragStart, false);
ui_card_back.addEventListener("mouseup", dragEnd, false);
ui_card_back.addEventListener("mousemove", drag, false);
