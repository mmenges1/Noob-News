function section(section) {
    alert("hello baby");
    var i;
    var x = document.getElementsByClassName('section');
    var y = section +'Tab';
    for (i = 0; i < x.length; i++) {
       x[i].style.display = 'none';
    }
    document.getElementById('GeneralTab').classList.remove('active');
    document.getElementById('FamilyTab').classList.remove('active');
    document.getElementById('CommentTab').classList.remove('active');
    document.getElementById('PurchasedTab').classList.remove('active');
    document.getElementById(section).style.display = 'block';
    document.getElementById(y).className = 'active';
}
