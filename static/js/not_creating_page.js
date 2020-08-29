function handleErrors(response) {
    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
}

function add_enter(element_id, call) {
    document.getElementById(element_id).onkeypress = function(e) {
        if(e.keyCode == 13) {
            call();
        }
    }
}

// add_enter('bet_amount', create);
// add_enter('event_name', create);

function create() {
    var bet_amount = document.getElementById('bet_amount').value;
    var event_name = document.getElementById('event_name').value;
    var entry = {
        bet_amount: bet_amount,
        event_name: event_name
    };
    console.log(entry)
    fetch('/create', {
        method: "POST",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(entry),
    })
    .then(response => location.reload(true));
}

function logout() {
    fetch('http://localhost:5000/logout')
    .then(function(data) {
        window.location.href = '/';
    });
}

var logo = document.getElementById('logo');
logo.addEventListener('click', home);
function home() {
    console.log('hi')
    fetch('http://localhost:5000/')
    .then(function(data) {
        window.location.href = '/';
    });
}

var created_bets_Btn = document.getElementById('created_bets_Btn');
created_bets_Btn.addEventListener('click', created_bets);
function created_bets() {
    console.log('hi')
    fetch('http://localhost:5000/created_bets')
    .then(function(data) {
        window.location.href = '/created_bets';
    });
}

var bets_engaged_in_Btn = document.getElementById('bets_engaged_in_Btn');
bets_engaged_in_Btn.addEventListener('click', bets_engaged_in);
function bets_engaged_in() {
    console.log('hi')
    fetch('http://localhost:5000/bets_engaged_in')
    .then(function(data) {
        window.location.href = '/bets_engaged_in';
    });
}

var private_bets_Btn = document.getElementById('private_bets_Btn');
private_bets_Btn.addEventListener('click', private_bets);
function private_bets() {
    console.log('hi')
    fetch('http://localhost:5000/private_bets')
    .then(function(data) {
        window.location.href = '/private_bets';
    });
}

var profile_Btn = document.getElementById('profile_Btn');
profile_Btn.addEventListener('click', profile);
function profile() {
    fetch('http://localhost:5000/profile')
    .then(function(data) {
        window.location.href = '/profile';
    });
}

function accept(ele) {
    var bet_id = ele.id
    console.log(ele.id)
    var entry = {
        bet_id: bet_id,
    };
        fetch('/accept', {
        method: "POST",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(entry),
    })
    .then(response => console.log(response.data));
}

function agree(ele) {
    var bet_id = ele.id
    console.log(ele.id)
    var entry = {
        bet_id: bet_id,
    };
        fetch('/agree', {
        method: "POST",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(entry),
    })
    .then(response => console.log(response.data));
}