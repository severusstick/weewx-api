<?php

namespace App\Http\Controllers;

use App\WeatherPerMinute;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class WeatherPerMinuteController extends Controller
{

    public function showAll()
    {
        return response()->json(WeatherPerMinute::all());
    }

    public function showOne($id)
    {
        return response()->json(WeatherPerMinute::find($id));
    }

    public function showLatest()
    {
        return response()->json([
			'latest_values' => WeatherPerMinute::latest()->first(),
			'min_max_average_values' => [
				'max' => [
					'barometer' => WeatherPerMinute::where('created_at', '>', Carbon::today())->max('barometer'),
					'outTemp' => WeatherPerMinute::where('created_at', '>', Carbon::today())->max('outTemp'),
					'outHumidity' => WeatherPerMinute::where('created_at', '>', Carbon::today())->max('outHumidity'),
					'dewpoint' => WeatherPerMinute::where('created_at', '>', Carbon::today())->max('dewpoint')
				],
				'min' => [
					'barometer' => WeatherPerMinute::where('created_at', '>', Carbon::today())->min('barometer'),
					'outTemp' => WeatherPerMinute::where('created_at', '>', Carbon::today())->min('outTemp'),
					'outHumidity' => WeatherPerMinute::where('created_at', '>', Carbon::today())->min('outHumidity'),
					'dewpoint' => WeatherPerMinute::where('created_at', '>', Carbon::today())->min('dewpoint')
				],
				'average' => [
					'barometer' => WeatherPerMinute::where('created_at', '>', Carbon::today())->avg('barometer'),
					'outTemp' => WeatherPerMinute::where('created_at', '>', Carbon::today())->avg('outTemp'),
					'outHumidity' => WeatherPerMinute::where('created_at', '>', Carbon::today())->avg('outHumidity'),
					'dewpoint' => WeatherPerMinute::where('created_at', '>', Carbon::today())->avg('dewpoint')
				]
			]
		]);
    }

    public function returnCallback()
	{
		//calculate callback time
		$created_time = WeatherPerMinute::where('created_at', '>', Carbon::today())->max('created_at');
		$archive_interval = 300;
		if ($created_time != NULL){
			$created_time = explode(' ', $created_time);
			$created_time = $created_time[1];
			$current_time = Carbon::now()->toTimeString();
			if ($created_time > $current_time){
				$callback_time = 60;
			}else{
				$created_time = explode(':', $created_time);
				$current_time = explode(':', $current_time);
				$next_refresh_time = ($created_time[0] * 3600 + $created_time[1] * 60 + $created_time[2]) + $archive_interval;
				$callback_time = $next_refresh_time - ($current_time[0] * 3600 + $current_time[1] * 60 + $current_time[2]);
				if ($callback_time <= 0) $callback_time = 60;
			}
		}else{
			$callback_time = 60;
		}

		return response()->json([
			'latest_id' => WeatherPerMinute::latest()->first('id'),
			'callback_time' => $callback_time
		]);
	}

    public function create(Request $request)
    {
        $weather = WeatherPerMinute::create($request->all());
 
        return response()->json($weather, 201);
    }

    public function update($id, Request $request)
    {
        $weather = WeatherPerMinute::findOrFail($id);
        $weather->update($request->all());

        return response()->json($weather, 200);
    }

    public function delete($id)
    {
        WeatherPerMinute::findOrFail($id)->delete();
        return response('Deleted Successfully', 200);
    }
}
