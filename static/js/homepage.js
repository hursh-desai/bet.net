function add_enter(element_id, call) {
    if (document.getElementById(element_id) == null) {return;}
    document.getElementById(element_id).onkeypress = function(e) {
        if(e.keyCode == 13) {
            call();
        }
    }
}

add_enter('bet_amount', create);
add_enter('event_name', create);
add_enter('mod_name', create);

function create() {
    var bet_amount = document.getElementById('bet_amount').value;
    var event_name = document.getElementById('event_name').value;
    var mod_name = document.getElementById('mod_name').value;
    var entry = {
        bet_amount: bet_amount,
        event_name: event_name,
        mod_name: mod_name
    };
    fetch('/create', {
        method: "POST",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(entry),
    })
    .then(response => {
        response.json().then(function (data){
            console.log(data)
        });
    });
}

function accept(ele) {
    var bet_id = ele.id
    ele.style.display = 'none ';
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

function user(ele){  
    var user = ele.id
    window.location.href = '/user/' + user;
}

function eventname(ele){
    var eventname = ele.id
    console.log('/event/' + eventname)
    window.location.href = '/eventname/' + eventname;
}
