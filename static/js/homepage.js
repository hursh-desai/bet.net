function add_enter(element_id, call) {
    ele = document.getElementById(element_id)
    if (ele == null) {return;}
    ele.onkeypress = function(e) {
        if(e.keyCode == 13) {
            call();
        }
    }
}

function not_hover(ele) {ele.setAttribute('src', '/static/img/handshake.png')}
function hover(ele) {ele.setAttribute('src', '/static/img/handshake2.png')}
function user(ele){window.location.href = '/user/' + ele.id}
function eventname(ele){window.location.href = '/eventname/' + ele.id}
add_enter('bet_amount', create_bet);
add_enter('event_name', create_event);
add_enter('mod_name', create_event);

async function create_event() {
    error.innerHTML = ''
    var event_name = document.getElementById('event_name').value;
    var mod_name = document.getElementById('mod_name').value;
    var entry = {
        event_name: event_name,
        mod_name: mod_name
    };

    response = await fetch('/create_event', {
        method: "POST",
        redirect: 'follow',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(entry),
    });
    json = await response.json();

    if (!response.ok) {
        error.innerHTML = json.error
    }
    else {window.location.href = '/eventname/' + event_name;}
}

async function create_bet() {
    var event_name = document.getElementsByClassName('bet_event_name')[0].getAttribute('name');
    var bet_amount = document.getElementById('bet_amount').value;
    var yes = document.getElementById('yes').checked;
    var no = document.getElementById('no').checked;
    if (yes == true) {
        var y_n = true;
    }
    else if (no == true) {
        var y_n = false;
    }
    else {var y_n = null;}
    var entry = {
        event_name: event_name,
        bet_amount: bet_amount,
        y_n: y_n,
    };
    response = fetch('/create_bet', {
        method: "POST",
        redirect: 'follow',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(entry),
    })
    json = await response.json();
    if (!response.ok) {
        error.innerHTML = json.error
    }
    else{location.reload(true);}
}

function accept(ele) {
    var bet_id = ele.getAttribute('name');
    // ele.style.display = 'none ';
    console.log(bet_id)
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
    .then(response => location.reload(true));
}

function agree(ele) {
    var agreement_id = ele.getAttribute('id');
    var entry = {
        agreement_id: agreement_id,
    };
    console.log(entry);
        fetch('/agree', {
        method: "POST",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(entry),
    })
    .then(response => location.reload(true));
}

function reject(ele) {
    var agreement_id = ele.getAttribute('id');
    var entry = {
        agreement_id: agreement_id,
    };
    console.log(entry);
        fetch('/reject', {
        method: "POST",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(entry),
    })
    .then(response => location.reload(true));
}

async function decide(ele) {
    var event_id = ele.getAttribute('id');
    var decider = ele.getAttribute('decider');
    if (decider == 'true') {
        var decision = true;
    }
    else if (decider == 'false') {
        var decision = false;
    }
    else {var decision = null;}
    var entry = {
        event_id: event_id,
        decision: decision
    };
    response = await fetch('/decision', {
        method: "POST",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(entry),
    });
    json = await response.json();
    location.reload(true);
}

