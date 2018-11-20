<template>
    <section>

        <pulse-loader :loading="loading" size="21px"></pulse-loader>

        <button class="button" v-if="converted" @click="doConvert">Convert</button>
        <div class="card-body">
            <div class="messages">
                <p><span class="font-weight-bold">{{ message }} </span></p>
            </div>
        </div>

        <span class="is-centered" v-if=" finished  === true">
                    <a :href="link"> {{link}}</a>
            <!--<button class="button" style="margin-right: 12.25px" @click="">Download</button>-->
        </span>
    </section>
</template>


<script>
    import axios from 'axios';
    import PulseLoader from 'vue-spinner/src/PulseLoader'

    export default {
        components: {PulseLoader},
        props: ['uuid'],
        data() {
            return {
                dropFiles: [],
                uploaded: false,
                status:'',
                isConnected: false,
                message:'Ready to convert.',
                messages:[],
                socket : null,
                finished: false,
                link: '',
                converted: true,
                loading: false
            }
        },
        comments: {
            PulseLoader
        },
        methods: {
            createWebSocket(uuid) {
                const ws = new WebSocket("ws://localhost:5555/progress/socket?uuid="+uuid)
                ws.onopen = function() {
                    // ws.send("Ready to start");
                    console.log("connecting to socket")
                };
                ws.onmessage = (evt) => {
                    console.log(evt.data)
                    console.log(this.message)
                    this.message = evt.data
                };
                this.socket = ws
            },
            doConvert(){
                console.log(this.uuid)
                const data = {
                    'uuid': this.uuid,
                    'file': this.uuid+".tar.gz"
                }
                axios.post("http://localhost:5000/createtxt",data).then( res => {
                    console.log(res.data)
                })
                this.converted = false
                this.loading = true
            },
        },
        watch: {
            message(){
                console.log(this.message)
                if (this.message === 'file is ready to download') {
                    this.finished = true
                    this.link = 'http://localhost:5555/download?uuid='+this.uuid
                    this.loading = false
                }
                if (this.message !== 'Ready to convert.' && this.message !== 'Starting Converting ...'){
                    this.converted = false
                }
            }
        },
        mounted() {
            if(this.socket) {
                console.log("hello from mounted")
                this.socket.onmessage = function (evt) {
                    this.message = evt.data
                }
            }else{
                this.createWebSocket(this.uuid)
            }
        }
    }
</script>

<!--<style scoped>-->

<!--</style>-->