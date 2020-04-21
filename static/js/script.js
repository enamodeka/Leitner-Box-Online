/**
 * UI VARIABLES
 */
const ui_btn_add_to_deck = document.querySelector('#ui_btn_add_to_deck');
const ui_btn_update_card = document.querySelector('#ui_btn_update_card');
const ui_btn_flip = document.querySelector('#ui_btn_flip');
const ui_card_front = document.querySelector('#ui_card_front');
const ui_card_back = document.querySelector('#ui_card_back');
const ui_text_front = document.querySelector('#ui_text_front');
const ui_text_back = document.querySelector('#ui_text_back');

/**
 * STATE VARIABLES
 */
let card_flip = false;

/**
 * LISTENERS
 */
ui_btn_flip.addEventListener('click', function(e) {
  console.log('Click')
  e.preventDefault();
  if(!card_flip) {
    ui_card_front.classList.add('card__front--hide');
    ui_card_back.classList.add('card__back--show');
    card_flip = true;
  } else {
    ui_card_back.classList.remove('card__back--show');
    ui_card_front.classList.remove('card__front--hide');
    card_flip = false;
  }
}
)
if(ui_btn_add_to_deck != null) {
  ui_btn_add_to_deck.addEventListener('click', function(e) {
    console.log('Click')
    e.preventDefault();
    console.log('Unescaped front text:', ui_text_front.innerHTML.replace(/\s+/g, " "));
    const data = {
      "text_front": ui_text_front.innerHTML.replace(/\s+/g, " "),
      "text_back": ui_text_back.innerHTML.replace(/\s+/g, " ")
    }
    console.log('Data ready to stringify', data);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/add-card');
    xhr.setRequestHeader('Content-type', 'application/json');
    const dataToSend = JSON.stringify(data);
    console.log('Data to send', dataToSend);
    xhr.send(dataToSend);
    xhr.onload = function() {
      if(xhr.status === 200){
        console.log('Response sunccessful')
        window.location.href = '/card-added';
      }
    }
  })
}

if(ui_btn_update_card != null) {
  ui_btn_update_card.addEventListener('click', function(e) {
    e.preventDefault();
    card_id = this.getAttribute('card_id');
    alert(card_id);
    console.log('Click')
    console.log('Unescaped front text:', ui_text_front.innerHTML.replace(/\s+/g, " "));
    const data = {
      "card_id": card_id,
      "text_front": ui_text_front.innerHTML.replace(/\s+/g, " "),
      "text_back": ui_text_back.innerHTML.replace(/\s+/g, " ")
    }
    console.log('Data ready to stringify', data);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/update-card');
    xhr.setRequestHeader('Content-type', 'application/json');
    const dataToSend = JSON.stringify(data);
    console.log('Data to send', dataToSend);
    xhr.send(dataToSend);
    xhr.onload = function() {
      if(xhr.status === 200){
        console.log('Response sunccessful. Card updated.')
        // window.location.href = '/card-added';
      }
    }
  })
}

