const eye=document.getElementById("togglePassword");
const password=document.getElementById("password");
eye.onclick=function(){
    if(password.type==="password"){
        password.type="text";
        eye.classList.replace("bx-hide","bx-show");
    }else{
        password.type="password";
        eye.classList.replace("bx-show","bx-hide");
    }
}
document.getElementById("loginForm").addEventListener("submit",function(e){
    e.preventDefault();
    const username=document.getElementById("username").value.trim();
    const password=document.getElementById("password").value.trim();
    const role=document.getElementById("role").value;
    if(username===""){
        alert("Vui lòng nhập tài khoản");
        return;
    }
    if(password===""){
        alert("Vui lòng nhập mật khẩu");
        return;
    }
    console.log({
        username,
        password,
        role
    });
});