function add_enter(element_id, call) {
    document.getElementById(element_id).onkeypress = function(e) {
        if(e.keyCode == 13) {
            call();
        }
    }
}

add_enter('username', login);
add_enter('password', login);
add_enter('new_username', sign_up);
add_enter('new_password', sign_up);

function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var entry = {
        username: username,
        password: password
    };
    fetch('http://localhost:5000/login', {
        method: "POST",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(entry),
    })
    .then(response => location.reload(true));
}

function sign_up() {
    var username = document.getElementById('new_username').value;
    var password = document.getElementById('new_password').value;
    var entry = {
        username: username,
        password: password
    };
    fetch('http://localhost:5000/sign_up', {
        method: "POST",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(entry),
    })
    .then(response => location.reload(true));
}

var login_modal = document.getElementById('login-modal');
var login_Btn = document.getElementById('login-Btn');
var closeBtn = document.getElementsByClassName('closeBtn')[0];

login_Btn.addEventListener('click', openModal);
closeBtn.addEventListener('click', closeModal);
window.addEventListener('click', clickOutside);

function openModal() {
    login_modal.style.display = 'block';
}
function closeModal() {
    login_modal.style.display = 'none ';
}
function clickOutside(e) {
    if(e.target == login_modal){
        closeModal();
    }
}


var sign_up_modal = document.getElementById('sign-up-modal');
var sign_up_Btn = document.getElementById('sign-up-Btn');
var closeBtn = document.getElementsByClassName('closeBtn')[1];

sign_up_Btn.addEventListener('click', open_SU_Modal);
closeBtn.addEventListener('click', close_SU_Modal);
window.addEventListener('click', click_SU_Outside);

function open_SU_Modal() {
    sign_up_modal.style.display = 'block';
}
function close_SU_Modal() {
    sign_up_modal.style.display = 'none ';
}
function click_SU_Outside(e) {
    if(e.target == sign_up_modal){
        close_SU_Modal();
    }
}

var need_to_sign_up_Btn = document.getElementById('need_to_sign_up');
need_to_sign_up_Btn.addEventListener('click', need_to_sign_up);
function need_to_sign_up() {
    closeModal();
    open_SU_Modal();
}

var already_has_account_Btn = document.getElementById('already_has_account');
already_has_account_Btn.addEventListener('click', already_has_account);
function already_has_account() {
    close_SU_Modal();
    openModal();
}

function cant_agree() {
    openModal();
}