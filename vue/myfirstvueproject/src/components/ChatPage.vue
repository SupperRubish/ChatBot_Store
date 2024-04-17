<template>
     <div class="talk_con">
        <div class="talk_show" id="words">
            <div :class="[(i.person=='you')?'chatbot':'people']" v-for="i in list1">
              <span :class="">{{i.person}}：{{i.say}}</span>
              <br>
              <table v-if="i.data.length > 0" class="Buy-table">
                <tr>
                  <th>name</th>
                  <th>color</th>
                  <th>kind</th>
                  <th>price</th>
                  <th>Size</th>
                  <th>Action</th>
                </tr>
                <tr v-for="row in i.data">
                  <!-- 根据你的数据结构，这里应该列出所有数据列 -->
                  <td>{{ row.name }}</td>
                  <td>{{ row.color }}</td>
                  <td>{{ row.kind }}</td>
                  <td>{{ row.price }}</td>
                  <td>{{ row.size }}</td>
                  <td><button @click="BUY(row.id)" class="Buy-button">BUY</button></td>
                  <!-- 其他数据 -->
                </tr>
              </table>

              <div v-if="i.select" class="selection-area">
                  <select  v-model="choose_id_user" name="fruit" class="select-input">
                  <option value="1">Order ID</option>
                  <option value="2">Username</option>
                  </select>
                  <input  v-model="order" class="text-input" placeholder="Order ID or Username">
                  <input  type="button" value="select" class="order_sub" id="odersub" @click="orderselect">
              </div>
              <table v-if="i.orderdata.length > 0" class="Buy-table">
                <tr>
                  <th>Order ID</th>
                  <th>Name</th>
                  <th>ProductName</th>
                  <th>Address</th>
                  <th>price</th>
                  <th>kind</th>
                  <th>color</th>
                  <th>Date</th>
                  <th>Action</th>
                  <th>Actions</th>
                </tr>
                <tr v-for="row in i.orderdata">
                  <!-- 根据你的数据结构，这里应该列出所有数据列 -->
                  <td>{{ row.OrderID }}</td>
                  <td>{{ row.Username }}</td>
                  <td>{{ row.productName }}</td>
                  <td>{{ row.address}}</td>
                  <td>{{ row.price }}</td>
                  <td>{{ row.kind }}</td>
                  <td>{{ row.color }}</td>
                  <td>{{ row.date }}</td>
<!--                  <td><button @click="Refund(row.OrderID)" class="Refund-button">Refund</button></td>-->
                  <td><button  @click="Refund(row.OrderID)" :title="row.canRefund ? 'Click to refund' : 'Refund is not available because of time out'"  :class="{ 'Refund-button': true, 'disabled': !row.canRefund }">Refund</button></td>
                  <!-- 其他数据 -->
                </tr>
              </table>
            </div>
            <!-- <div class="btalk"><span>B说：还没呢，你呢？</span></div> -->
        </div>
        <div class="talk_input">
            <input type="text" class="talk_word" id="talkwords" v-model="text1">
            <!-- 绑定单击监听,把value传到vue的list1中 -->
            <input type="button" value="send" class="talk_sub" id="talksub" @click="fnAdd">
        </div>
    </div>
</template>

<!--<script type="text/javascript">-->
<script type="text/javascript">

 export default {
  //定义当前vue数据,每个实例数据是独立的
  data() {
   return {
    list1:[{person:'Chatbot',say:'Please input your username first, thank you!',data:[],orderdata:[]},
    ],
    sel1:0,
    text1:'',
    login:false,
    order:'',
    choose_id_user:''
   }
  },

methods:{
        fnAdd:function(){
          if(this.text1 == ''){
                alert("请输入内容!");
                return;
            }
          if(this.login==false){
              let self = this;
              let text = this.text1
              self.list1.push({person:'you',say:this.text1,data:[],select:false,orderdata:[]})
              console.log(text)

              this.$axios.post('http://localhost:8000/login/', this.$qs.stringify({
                      username: text,
            }))
            .then(function(response) {
                console.log(response['data']);
                var responses = response['data']
                if(responses['login']===true){
                    self.login=true
                }
                 self.list1.push({person:'Chatbot:',say:responses['reply'],data:responses['data'],select:false,orderdata:[]})
                  self.scrollToBottom();
					  })
					.catch(function(err) {
						//请求失败
						console.log('Error:', err);
					});
              this.text1=''
          }
          else {
              var self = this;

            // 列表追加数据push()
            this.list1.push({person:'you',say:this.text1 ,data:[],select:false,orderdata:[]});
            self.scrollToBottom();

            this.$axios.post('http://localhost:8000/Ask/', this.$qs.stringify({
                      Ask: this.text1
            }))
            .then(function(response) {
                console.log(response);
                var response = response['data']
                if (response['data']!="") {
                    self.list1.push({person:'Chatbot:',say:response['reply'],data:response['data'],select:response['select'],orderdata:[]});
                    self.scrollToBottom();
                }
                else {
                    self.list1.push({person:'Chatbot:',say:response['reply'],data:[],select:response['select'],orderdata:[]})
                    self.scrollToBottom();
                }

					  })
            .catch(function(err) {
						//请求失败
						console.log('Error:', err);
					});
            this.text1='';
          }


        },
        BUY:function (id){
            let self = this;
            console.log(id)
            this.$axios.post('http://localhost:8000/buy/', this.$qs.stringify({
                        pid: id
              }))
            .then(function(response) {
                  console.log(response)
                  self.list1.push({person:'Chatbot:',say:response['data']['reply'],data:[],orderdata:[]})
                  self.scrollToBottom();
              })

            .catch(function(err) {
              //请求失败
              console.log('Error:', err);
            });

        },
        Refund:function (id){
            let self = this;
            console.log(id)
            this.$axios.post('http://localhost:8000/refund/', this.$qs.stringify({
                        orderid: id
              }))
            .then(function(response) {
                  console.log(response)
                  self.list1.push({person:'Chatbot:',say:response['data']['reply'],data:[],orderdata:[]})
                  self.scrollToBottom();
              })

            .catch(function(err) {
              //请求失败
              console.log('Error:', err);
            });

        },

        orderselect:function (){
          console.log(this.choose_id_user)
          console.log(this.order)
          var self = this
          this.$axios.post('http://localhost:8000/order/',this.$qs.stringify({
            choose:self.choose_id_user,
            select:self.order
          }))
            .then(function (response){
              self.list1.push({person:'Chatbot:',say:response['data']['reply'],data:[],orderdata:response['data']['orderdata']})
              self.scrollToBottom();
            })
          .catch(function(err) {
              //请求失败
              console.log('Error:', err);
            });

        },

        scrollToBottom: function() {
          const chatContainer = this.$el.querySelector("#words");
          chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }
 }
</script>

<style>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.people, .chatbot {
  animation: fadeIn 0.5s ease-out;
}

.talk_con {
  box-shadow: 0 0 15px rgba(0,0,0,0.2);
  border-radius: 8px;
  overflow: hidden;
  width: 950px;
  height: 540px;
  border: 1px solid #666;
  margin: 50px auto 0;
  background: #f9f9f9;
}

.talk_input {
  display: flex;
  align-items: center;
  padding: 10px;
     width: 650px;
            margin: 10px auto 0;
}

.talk_show {
  padding: 20px;
}
.talk_word, .talk_sub {
  border: 1px solid #ccc;
  border-radius: 20px;
  padding: 5px 10px;
  margin-right: 10px;
  outline: none;
  transition: border-color 0.3s;
}

.talk_sub {
  cursor: pointer;
  background-color: #0181cc;
  color: white;
  border: none;
  width: 250px;
  height: 30px;
  float: left;
  margin-left: 10px;
}

.talk_word:focus, .talk_sub:hover {
  border-color: #0181cc;
}

.people span, .chatbot span {
  background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
  color: #333;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  border-radius: 18px;
  padding: 10px 15px;
  max-width: 80%;
  display: inline-block;
  margin: 5px;
}

.talk_show {
  border: none;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  width: 900px;
  height: 420px;
  border: 1px solid #666;
  background: #fff;
  margin: 10px auto 0;
  overflow: auto;
}

/* 适应性布局，让文字不会溢出 */
.talk_word {
  width: calc(100% - 150px); /* 调整输入框宽度，确保按钮不会挤到下一行 */
  width: 800px;
  height: 26px;
  padding: 0px;
  float: left;
  margin-left: 10px;
  outline: none;
  text-indent: 10px;
}


.whotalk {
    width: 80px;
    height: 30px;
    float: left;
    outline: none;
}

.people {
    margin: 10px;
    text-align: left;
}

.people span {
    display: inline-block;
    background: #0181cc;
    border-radius: 10px;
    color: #fff;
    padding: 5px 10px;
}

.chatbot {
    margin: 10px;
    text-align: right;
}

.chatbot span {
    display: inline-block;
    background: #ef8201;
    border-radius: 10px;
    color: #fff;
    padding: 5px 10px;
}

.Buy-table {
  border-collapse: collapse;
  margin: 25px 0;
  font-size: 0.9em;
  font-family: sans-serif;
  min-width: 400px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}

.Buy-table thead tr {
  background-color: #009879;
  color: #ffffff;
  text-align: left;
}

.Buy-table th,
.Buy-table td {
  padding: 12px 15px;
}

.Buy-table tbody tr {
  border-bottom: 1px solid #dddddd;
}

/* Zebra striping for rows */
.Buy-table tbody tr:nth-of-type(even) {
  background-color: #f3f3f3;
}

.Buy-table tbody tr:last-of-type {
  border-bottom: 2px solid #009879;
}

.Buy-table tbody tr.active-row {
  font-weight: bold;
  color: #009879;
}

.Buy-button {
  background-color: #009879;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.Buy-button:hover {
  background-color: #007f6b;
}

.Refund-button {
  background-color: hotpink;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}
.Refund-button.disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.Refund-button:hover {
  background-color: #007f6b;
}
.selection-area {
  display: flex;
  justify-content: start;
  align-items: center;
  gap: 10px; /* 为每个元素添加间隙 */
  padding: 10px;
}

.select-input, .text-input, .order_sub {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
  transition: border-color 0.3s ease;
}

.select-input:focus, .text-input:focus {
  border-color: #009879;
}

.order_sub {
  background-color: #009879;
  color: white;
  border: none;
  cursor: pointer;
}

.order_sub:hover {
  background-color: #007f6b;
}

/* 针对小屏幕的响应式布局 */
@media (max-width: 768px) {
  .selection-area {
    flex-direction: column;
  }

  .select-input, .text-input, .order_sub {
    width: 100%; /* 在移动设备上全宽 */
    margin-bottom: 10px; /* 增加垂直间隙 */
  }

  .order_sub {
    padding: 10px 20px; /* 为按钮添加更多内边距 */
  }
}

</style>
