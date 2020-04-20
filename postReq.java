OkHttpClient client = new OkHttpClient().newBuilder()
  .build();
MediaType mediaType = MediaType.parse("application/json,text/plain");
RequestBody body = RequestBody.create(mediaType, "{\n \"name\" : \"newname10\",\n \"birthplace\" : \"atx\"\n}");
Request request = new Request.Builder()
  .url("https://es96app.herokuapp.com/test")
  .method("POST", body)
  .addHeader("Content-Type", "application/json")
  .addHeader("Content-Type", "text/plain")
  .build();
Response response = client.newCall(request).execute();