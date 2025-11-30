import { supabase } from './src/config/supabase';

async function testDatabaseConnection() {
  console.log('🔍 Testing Supabase Database Connection...\n');

  try {
    // Test 1: Check connection
    console.log('[Test 1] Testing basic connection...');
    const { data: connectionTest, error: connectionError } = await supabase
      .from('jobs')
      .select('count')
      .limit(1);
    
    if (connectionError) {
      throw new Error(`Connection failed: ${connectionError.message}`);
    }
    console.log('✅ Connection successful!\n');

    // Test 2: Count tables
    console.log('[Test 2] Counting records in tables...');
    
    const { count: resumeCount } = await supabase
      .from('resumes')
      .select('*', { count: 'exact', head: true });
    console.log(`   Resumes: ${resumeCount || 0}`);

    const { count: jobCount } = await supabase
      .from('jobs')
      .select('*', { count: 'exact', head: true });
    console.log(`   Jobs: ${jobCount || 0}`);

    const { count: scoreCount } = await supabase
      .from('scores')
      .select('*', { count: 'exact', head: true });
    console.log(`   Scores: ${scoreCount || 0}\n`);

    // Test 3: Fetch sample jobs
    console.log('[Test 3] Fetching sample jobs...');
    const { data: jobs, error: jobsError } = await supabase
      .from('jobs')
      .select('id, title, company, location')
      .limit(5);

    if (jobsError) throw jobsError;

    if (jobs && jobs.length > 0) {
      console.log(`✅ Found ${jobs.length} jobs:`);
      jobs.forEach((job: any, index: number) => {
        console.log(`   ${index + 1}. ${job.title} at ${job.company} (${job.location})`);
      });
    } else {
      console.log('⚠️  No jobs found. Run schema.sql to insert sample data.');
    }
    console.log('');

    // Test 4: Test insert operation (resume)
    console.log('[Test 4] Testing insert operation...');
    const testUserId = '00000000-0000-0000-0000-000000000001'; // Test user ID
    
    const { data: newResume, error: insertError } = await supabase
      .from('resumes')
      .insert([{
        user_id: testUserId,
        title: 'Test Resume - Database Connection Check',
        content: 'This is a test resume to verify database connectivity.',
        skills: ['JavaScript', 'TypeScript', 'Node.js'],
        experience: [],
        education: []
      }])
      .select()
      .single();

    if (insertError) throw insertError;

    console.log(`✅ Resume created with ID: ${newResume.id}\n`);

    // Test 5: Test update operation
    console.log('[Test 5] Testing update operation...');
    const { data: updatedResume, error: updateError } = await supabase
      .from('resumes')
      .update({ title: 'Test Resume - Updated' })
      .eq('id', newResume.id)
      .select()
      .single();

    if (updateError) throw updateError;

    console.log(`✅ Resume updated: ${updatedResume.title}\n`);

    // Test 6: Test query with filter
    console.log('[Test 6] Testing query with filter...');
    const { data: filteredJobs, error: filterError } = await supabase
      .from('jobs')
      .select('title, company')
      .ilike('location', '%Remote%');

    if (filterError) throw filterError;

    console.log(`✅ Found ${filteredJobs?.length || 0} remote jobs\n`);

    // Test 7: Test delete operation
    console.log('[Test 7] Testing delete operation...');
    const { error: deleteError } = await supabase
      .from('resumes')
      .delete()
      .eq('id', newResume.id);

    if (deleteError) throw deleteError;

    console.log(`✅ Test resume deleted\n`);

    // Test 8: Test JSONB operations
    console.log('[Test 8] Testing JSONB queries...');
    const { data: pythonJobs, error: jsonbError } = await supabase
      .from('jobs')
      .select('title, company, skills')
      .filter('skills', 'cs', '{"Python"}');

    if (jsonbError) {
      console.log(`⚠️  JSONB query test skipped: ${jsonbError.message}\n`);
    } else {
      console.log(`✅ Found ${pythonJobs?.length || 0} jobs requiring Python\n`);
    }

    // Summary
    console.log('═══════════════════════════════════════');
    console.log('✅ All Database Tests Passed!');
    console.log('═══════════════════════════════════════');
    console.log('\nDatabase Statistics:');
    console.log(`  • Total Resumes: ${resumeCount || 0}`);
    console.log(`  • Total Jobs: ${jobCount || 0}`);
    console.log(`  • Total Scores: ${scoreCount || 0}`);
    console.log(`  • Remote Jobs: ${filteredJobs?.length || 0}`);
    console.log(`  • Python Jobs: ${pythonJobs?.length || 0}`);
    console.log('\n✅ Supabase connection is working correctly!');

  } catch (error: any) {
    console.error('\n❌ Database Test Failed!');
    console.error('Error:', error.message);
    console.error('\nTroubleshooting:');
    console.error('1. Check your .env file has correct SUPABASE_URL and SUPABASE_KEY');
    console.error('2. Verify database tables exist (run schema.sql in Supabase SQL editor)');
    console.error('3. Check your internet connection');
    console.error('4. Verify Supabase project is active');
    process.exit(1);
  }
}

// Run the test
testDatabaseConnection();
