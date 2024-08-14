import $ from 'jquery'
import jwt_decode from 'jwt-decode'

const ModuleUser={
    state:{
        id:"",
        username:"",
        photo:"",
        followerCount:0,
        access:"",//令牌
        refresh:"",//刷新令牌
        is_login:false,//是否登录

    },
    getters:{

    },
    mutations:{
        updateUser(state,user){
            state.id=user.id;//忘写.id导致的wa
            state.username=user.username;
            state.photo=user.photo;
            state.followerCount=user.followerCount;
            state.access=user.access;
            state.refresh=user.fresh;
            state.is_login=user.is_login;
        },
        //actions不能直接修改state
        updateAccess(state,access){
            state.access=access;

        },
        logout(state){
            state.id="";
            state.username="";
            state.photo="";
            state.followerCount=0;
            state.access="";
            state.refresh="";
            state.is_login=false;


        }

    },
    actions:{
        //一开始放错了位置
          //登录
    login(context,data){
        $.ajax({
          url:"https://app165.acapp.acwing.com.cn/api/token/",
          type:"POST",//写成post，没加引号
          data:{
            username:data.username,
            password:data.password,
          
          },
          success(resp){
            //console.log(resp);
            //获取refresh和access
            const {access,refresh}=resp;
            //获取用户名
            //jwt验证
            const access_obj=jwt_decode(access);//解码
            //console.log(access_obj,refresh);//refresh也要输出
            //定期刷新更新access令牌
            setInterval(()=>{
                $.ajax({
                    url:"https://app165.acapp.acwing.com.cn/api/token/refresh/",
                    type:"POST",
                    data:{
                        refresh,
                    },
                    success(resp){
                        //console.log(resp);
                        //console.log("refresh started");
                        context.commit('updateAccess',resp.access);
                    }

                });

            },4.5*60*1000);
            $.ajax({
                url:"https://app165.acapp.acwing.com.cn/myspace/getinfo/",
                type:"GET",
                data:{
                    user_id:access_obj.user_id,

                },
                headers:{
                    'Authorization':"Bearer " +access, //注意空格
                },
                success(resp){
                    //console.log(resp);
                    context.commit("updateUser",{
                        ...resp,
                        access:access,
                        refresh:refresh,
                        is_login:true,
                    });
                    //调用回调函数
                    data.success();

                },
               
            })
          },
          error(){
            data.error();


        }
        });
  
      },
    

    },
    modules:{
         

    }

};
export default ModuleUser;