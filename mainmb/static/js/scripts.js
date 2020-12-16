function addTicket(MaCB, TenCB, MaDG, GiaTien,) {
    fetch('/add_ticket', {
        method: 'post',
        body: JSON.stringify({
            MaCB,
            TenCB,
            MaDG,
            GiaTien,
        }),
        headers: {
            'Context-Type': 'application/json',
        },
    })
        .then((res) => res.json())
        .then((data) => {
            console.info(data);
        })
        .catch((err) => {
            console.log(err);
        });
}


function commit(){

    fetch('/payment', {
        method: 'post',
        body: JSON.stringify({
            payment,
            position,
        }),
        headers: {
            'Context-Type': 'application/json',
        },
    })
    .then(res=>{
        location.href = '/payment'
    })
    .catch((err) => {
        console.log(err);
    });
}


