<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateWeatherPerMinuteTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('weather_per_minutes', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->double('barometer');
            $table->double('outTemp');
            $table->double('outHumidity');
            $table->double('windSpeed');
            $table->double('windDir');
            $table->double('windGust');
            $table->double('windGustDir');
            $table->double('dewpoint');
            $table->double('hourRain');
            $table->double('dayRain');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('weather_per_minutes');
    }
}
