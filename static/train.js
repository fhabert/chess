const init_train = () => {
    const content = document.querySelector('.uploading');
    if (content) {
        const btn_upload = document.getElementById("upload");
        btn_upload.addEventListener("change", async (e) => {
            if (e.target.files !== undefined) {
                // const url = URL.createObjectURL(e.target.files[0]);
                // let blob = await fetch(url).then(r => r.blob());
                var data = new FormData()
                data.append('file', e.target.files[0])
                // console.log(e.target.files[0]);
                // console.log(data);
                // content.innerHTML = "";
                // fetch("/get_pieces", {
                //     method:"POST",
                //     body: e.target.files[0]
                // })
            }
        })
        const btn_submit = document.getElementById("submit_btn");
        btn_submit.addEventListener("click", (e) => {
            e.preventDefault();
        })
    }
}
init_train();