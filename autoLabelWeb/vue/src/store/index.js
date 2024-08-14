import {createStore} from 'vuex'
import ModuleUser from './user';
// import {createPinia} from 'pinia';
// import piniaPersist from 'pinia-plugin-persist'
//
// const store = createPinia()
// store.use(piniaPersist)

export default createStore({
    state: {
        taskId: null,
        status: '',
        status2: '',
        total: 0,
        current: 0,
        loading: true,
        isLoading:true,
        tableData: [],
        lastPage: 1,
        currentPage: 1,
        isRefinery:false,
        labelMatch:''

    },
    getters: {
        getTaskId(state) {
            return state.taskId;
        },
        getStatus(state) {
            return state.status;
        },
        getStatus2(state) {
            return state.status2;
        },
        getTotal(state) {
            return state.total;
        },
        getCurrent(state) {
            return state.current;
        },
        getLoading(state) {
            return state.loading;
        },
        getIsLoading(state) {
            return state.isLoading;
        },
        getTableData(state) {
            return state.tableData;
        },
        getLastPage(state) {
            return state.lastPage;
        },
        getCurrentPage(state) {
            return state.currentPage;
        },
        getIsRefinery(state){
            return state.isRefinery;
        },
        getLabelMatch(state){
            return state.labelMatch;
        }
        //fullName(state){
        // return state.user.firstName+state.user.lastName;
        // }
    },
    mutations: {
        SET_TASKID(state, taskId) {
            state.taskId = taskId;
        },
        SET_STATUS(state, status) {
            state.status = status;
        },
        SET_STATUS2(state, status2) {
            state.status2 = status2;
        },
        SET_TOTAL(state, total) {
            state.total = total;
        },
        SET_CURRENT(state, current) {
            state.current = current;
        },
        SET_LOADING(state, loading) {
            state.loading = loading;
        },
        SET_ISLOADING(state, isLoading) {
            state.isLoading = isLoading;
        },
        SET_TABLEDATA(state, tableData) {
            state.tableData = tableData;
        },
        SET_LASTPAGE(state, lastPage) {
            state.lastPage = lastPage;
        },
        SET_CURRENTPAGE(state, currentPage) {
            state.currentPage = currentPage;
        },
        SET_ISREFINERY(state,isRefinery){
            state.isRefinery=isRefinery;
        },
        SET_LABELMATCH(state,labelMatch){
            state.labelMatch=labelMatch;
        }
        // updateUser(state,user){

        //}
    },
    actions: {
        setTaskId({commit}, status) {
            commit('SET_TASKID', status); // 触发 mutation 来更新状态
        },
        setStatus({commit}, status) {
            commit('SET_STATUS', status); // 触发 mutation 来更新状态
        },
        setStatus2({commit}, status2) {
            commit('SET_STATUS2', status2); // 触发 mutation 来更新状态
        },
        setTotal({commit}, total) {
            commit('SET_TOTAL', total); // 触发 mutation 来更新状态
        },
        setCurrent({commit}, current) {
            commit('SET_CURRENT', current); // 触发 mutation 来更新状态
        },
        setLoading({commit}, loading) {
            commit('SET_LOADING', loading);
        },
        setIsLoading({commit}, isloading) {
            commit('SET_ISLOADING', isloading);
        },
        setTableData({commit}, tableData) {
            commit('SET_TABLEDATA', tableData);
        },
        setLastPage({commit}, lastPage) {
            commit('SET_LASTPAGE', lastPage);
        },
        setCurrentPage({commit}, currentPage) {
            commit('SET_CURRENTPAGE', currentPage);
        },
        setIsRefinery({commit},isRefinery){
            commit('SET_ISREFINERY',isRefinery);
        },
        setLabelMatch({commit},labelMatch){
            commit('SET_LABELMATCH',labelMatch);
        }
    },

    persist:{
      enabled:true,
      strategies:[
          {
              storage:localStorage,
              paths:['isRefinery']
          }
      ]
    },
    //对state进行分割
    modules: {

        //users:{


        //}
        user: ModuleUser,
    }
})
